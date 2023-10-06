#!/usr/bin/env ruby
require 'json'
require 'net/http'

config_path = File.expand_path('../config.sample.json', __dir__)
config = JSON.parse(File.read(config_path))


path = "/#{config['database']}/#{config['table']}"

payload = {
  events: [
    {
      name: 'John Doe',
      age: 25,
      comment: 'hello, world',
      object: {lang: 'ruby'},
      array: %w[hello world]
    },
    {
      name: 'Jane Done',
      age: 23,
      comment: 'good morning',
      object: {lang: 'ruby'},
      array: %w[good morning]
    },
  ]
}

Net::HTTP.start(config["endpoint"], 443, use_ssl: true) do |http|
  headers = {
    "Authorization" => "TD1 #{config["apikey"]}",
    "Content-Type" => "application/vnd.treasuredata.v1+json",
    "Accept" => "application/vnd.treasuredata.v1+json",
  }
  res = http.post(path, JSON.dump(payload), headers)
  p res
  puts res.body
end
