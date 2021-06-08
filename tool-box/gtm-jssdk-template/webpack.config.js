const TerserPlugin = require("terser-webpack-plugin");
const path = require("path");

module.exports = {
  entry: "./index.js",
  output: {
    filename: "td-gtm.js",
    path: path.resolve(__dirname, "dist"),
    library: {
      type: "umd",
      name: "tdInstance",
    },
  },
  optimization: {
    minimize: true,
    minimizer: [
      new TerserPlugin({
        extractComments: false,
      }),
    ],
  },
  mode: "production",
};
