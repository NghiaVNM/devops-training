require 'webrick'
require 'json'

server = WEBrick::HTTPServer.new(Port: 80)

server.mount_proc '/' do |req, res|
  res['Content-Type'] = 'application/json'
  res.body = JSON.generate({
    message: 'Hello World from Ruby!',
    version: '1.0.0'
  })
end

server.mount_proc '/healthz' do |req, res|
  res['Content-Type'] = 'text/plain'
  res.body = 'ok'
end

trap('INT') { server.shutdown }

puts 'Server running on port 80'
server.start