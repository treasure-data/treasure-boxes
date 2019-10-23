import os
import textwrap


class FeatureSelector(object):
    def __init__(self):
        self.apikey = os.getenv("TD_API_KEY")
        self.endpoint = os.getenv("TD_API_SERVER")

    def run(self, dbname="boston", source_table="house_prices"):
        import pandas as pd
        import pytd.pandas_td as td
        from sklearn.ensemble import ExtraTreesRegressor
        from sklearn.feature_selection import SelectFromModel

        connection = td.connect(apikey=self.apikey, endpoint=self.endpoint)
        engine = td.create_engine(f"presto:{dbname}", con=connection)

        # Fetch 25% random sampled data
        df = td.read_td(
            f"""
            select *
            from {source_table} tablesample bernoulli(25)
            """,
            engine,
        )
        # You can use Hive instead:
        #
        # engine_hive = td.create_engine(f'hive:{dbname}', con=connection)
        # df = td.read_td(
        #     """
        #     select *
        #     from {}_train
        #     where rnd < 0.25
        #     """.format(source_table),
        #     engine_hive
        # )
        df = df.drop(columns=["time", "v", "rnd", "rowid"], errors="ignore")

        y = df.medv
        X = df.drop(columns=["medv"])

        categorical_columns = set(["rad", "chas"])
        quantitative_columns = set(X.columns) - categorical_columns

        reg = ExtraTreesRegressor()
        reg = reg.fit(X, y)

        feature_importances = pd.DataFrame(
            {"column": X.columns, "importance": reg.feature_importances_}
        )
        td.to_td(
            feature_importances,
            f"{dbname}.feature_importances",
            con=connection,
            if_exists="replace",
            index=False,
        )

        model = SelectFromModel(reg, prefit=True)

        feature_idx = model.get_support()
        feature_name = df.drop(columns=["medv"]).columns[feature_idx]
        selected_features = set(feature_name)

        categorical_columns = set(["rad", "chas"])
        quantitative_columns = set(X.columns) - categorical_columns

        feature_types = {
            "categorical_columns": categorical_columns,
            "quantitative_columns": quantitative_columns,
        }
        feature_query = self._feature_column_query(
            selected_features, feature_types=feature_types
        )

        # Store query if possible
        try:
            import digdag

            digdag.env.store({"feature_query": feature_query})

        except ImportError:
            pass

        # self._create_vectorize_table(
        #     engine_hive, dbname, "train", f"{source_table}_train",
        #     feature_query)
        # self._create_vectorize_table(
        #     engine_hive, dbname, "test", f"{source_table}_test",
        #     feature_query)

    def _create_vectorize_table(
        self, engine, dbname, table_name, source_table, feature_query
    ):
        import tdclient
        import pandas_td as td

        # Create feature vector table
        with tdclient.Client(apikey=self.apikey, endpoint=self.endpoint) as client:
            db = client.database(dbname)
            try:
                db.table(table_name)
                db.table(table_name).delete()
            except tdclient.api.NotFoundError as e:
                pass

            db.create_log_table(table_name)

        hql = f"""insert overwrite table {table_name}
        select
            rowid,
        {textwrap.indent(feature_query, '    ')},
            medv as price
        from
            {source_table}
        """

        td.read_td(hql, engine)

    def _feature_column_query(
        self, candidate_columns, feature_types=set(), normalize=None
    ):
        """Create feature columns vector query for Logistic/Linear Regression on Hivemall
        """

        def build_feature_array(columns, normalize=None, ctype="quantitative"):
            _query = ""
            _query += 'array("'
            _query += '", "'.join(columns)
            _query += '"),\n'

            if normalize == "log1p":
                if not ctype == "quantitative":
                    raise ValueError(
                        "ctype must be 'quantitative' if 'normalize' is used"
                    )

                _query += "ln("
                _query += "+1),\nln(".join(columns)
                _query += "+1)"

            else:
                _query += ",\n".join(columns)

            return f"{ctype}_features(\n{textwrap.indent(_query, '  ')}\n)"

        quantitative_columns = candidate_columns & feature_types["quantitative_columns"]
        categorical_columns = candidate_columns & feature_types["categorical_columns"]

        both_column_type = (len(quantitative_columns) > 0) and (
            len(categorical_columns) > 0
        )

        _query = ""

        if both_column_type:
            _query = "concat_array(\n"

        if len(quantitative_columns) > 0:
            feature_array = build_feature_array(
                quantitative_columns, normalize=normalize, ctype="quantitative"
            )
            if both_column_type:
                _query += textwrap.indent(feature_array, "  ")
            else:
                _query += feature_array

        if both_column_type:
            _query += ",\n"

        if len(categorical_columns) > 0:
            feature_array = textwrap.indent(
                build_feature_array(categorical_columns, ctype="categorical"), "  "
            )
            if both_column_type:
                _query += textwrap.indent(feature_array, "  ")
            else:
                _query += feature_array

        if both_column_type:
            _query += "\n)"

        _query += " as features"

        return _query


if __name__ == "__main__":
    FeatureSelector().run()
