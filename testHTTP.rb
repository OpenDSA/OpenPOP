def old
require 'net/http'
uri = URI("http://127.0.0.1:3000/exercises")

http = Net::HTTP.new(uri.host, uri.port)
req = Net::HTTP::Get.new(uri.path)
resp = http.request(req)#get request
#we can puts resp.body to see the results and resp.code to see the returned code


res = Net::HTTP.post_form(URI.parse('http://127.0.0.1:3000/exercises'),
                          {'exercise_id' => 'ru44by', 'code' => '54440'})

puts res.body

end


require 'net/http'
require 'json'

def create_agent
  uri = URI('https://192.168.33.10:9210/exercises')
  http = Net::HTTP.new(uri.host, uri.port)
  req = Net::HTTP::Post.new(uri.path, 'Content-Type' => 'application/json')
  req.body = {exercise_id: 'John Doe2', code: 'agen2t'}.to_json
  res = http.request(req)
  puts "response #{res.body}"
rescue => e
  puts "failed #{e}"
end

def visualize
  uri = URI('https://192.168.33.10:9210/answers/visualize')
  http = Net::HTTP.new(uri.host, uri.port)
  #http.use_ssl = true
  req = Net::HTTP::Post.new(uri.path, 'Content-Type' => 'application/json')
  req.body = { exercises: '2', answers: '5' }.to_json
  res = http.request(req)
  puts "response #{res.body}"
end

def tryHTTParty
  require 'httparty'
  require 'json'
  HTTParty.get('https://192.168.33.10:9210/exercises',
                :body => { :exercise_id => 'JHavePOPex1'}.to_json,
                :headers => { 'Content-Type' => 'application/json' }, :verify => false )
  puts request.parsed_response


end

def use_open_uri
  require 'open-uri'
  require 'openssl'
  params = {:exercise_id => 123, :code => 'asd'}
  request_uri=URI.parse("https://192.168.33.10:9210/answers/solve/#{params[:exercise_id]}/#{params[:code]}")

# The params incidentally are available as a String, via request_uri.query
  output = open(request_uri, {ssl_verify_mode: OpenSSL::SSL::VERIFY_NONE})
  obj = JSON.parse output.readlines.join("")
  puts obj
  render obj
end

def use_rest_client
  require 'rest-client'
  url = "https://192.168.33.10:9210/answers/solve"
  headers = {
      :content_type => "application/json",
      :"x-auth-token" => "testingtoken"
  }
  #r = RestClient.get url , {params: {'exercise_id' => 'qqqqqq', 'code' => "{p = p.next;}"}}, :verify_ssl => false

  res = RestClient::Request.execute(
      :url => url,
      :method => :get,
      :headers => headers,
      :verify_ssl => false
  )
  RestClient::Request.execute(
      :method => :get,
        :url => "https://192.168.33.10:9210/answers/solve",
        params: RestClient::ParamsArray.new([[:exercise_id => 'qqqqqq'],[:code => "{p = p.next;}"]]),
        :verify_ssl => false
  )
end

def use_rest_client_http
  require 'rest-client'

  uri = 'http://192.168.33.10:3000/answers/solve'
  exercise_id = 1
  r = RestClient.get url +'/' + String(exercise_id)

end
use_rest_client_http