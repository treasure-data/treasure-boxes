#!/bin/sh

td --apikey $TD_API_KEY table:create ${target} title_levenshtein

# at least, column `id` should exist for ../queries/levenshtein.sql
td --apikey $TD_API_KEY schema:add ${target} title_levenshtein id:string
