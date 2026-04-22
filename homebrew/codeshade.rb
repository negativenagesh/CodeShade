cask "codeshade" do
  version "0.1.0"
  
  # TODO: Update this SHA256 when you zip the .app file
  # You can generate this by running: shasum -a 256 CodeShade.app.zip
  sha256 "0000000000000000000000000000000000000000000000000000000000000000"

  # TODO: Update this to point to your GitHub releases URL where the zip is hosted
  url "https://github.com/your-username/codeshade/releases/download/v#{version}/CodeShade.app.zip"
  
  name "CodeShade"
  desc "Transparent Vibecoding Gambling Overlay"
  homepage "https://github.com/your-username/codeshade"

  app "CodeShade.app"

  zap trash: [
    "~/Library/Application Support/CodeShade",
    "~/Library/Preferences/com.your-username.codeshade.plist",
  ]
end
