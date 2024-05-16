# grab_gem_versions.rb

# Method to fetch gem versions
def fetch_gem_versions(gems)
    gem_versions = {}
    gems.each do |gem_name|
      begin
        spec = Gem::Specification.find_by_name(gem_name)
        gem_versions[gem_name] = spec.version.to_s
      rescue Gem::LoadError
        gem_versions[gem_name] = "Not installed"
      end
    end
    gem_versions
  end
  
  # List of gems you want to get versions for
  gems_to_check = ['net-http', 'uri', 'nokogiri', 'tk', 'zip']
  
  # Fetch versions for the specified gems
  gem_versions = fetch_gem_versions(gems_to_check)
  
  # Write gem versions to a file
  File.open('gem_versions.txt', 'w') do |file|
    gem_versions.each do |gem_name, version|
      file.puts "#{gem_name}: #{version}"
    end
  end
  
  puts "Gem versions have been written to gem_versions.txt"
  