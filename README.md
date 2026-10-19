# Black Shades Studio — GitHub / Netlify upload package

This package contains the complete dark photography website with all 134 photos, WhatsApp, phone and email links. The two assets ZIP files are uploaded as files; Netlify unpacks them automatically during the build. This avoids uploading hundreds of separate image files through GitHub's browser interface.

## Exactly what to upload

Extract `BlackShadesStudio-GitHub-Ready.zip` on your computer. Open the extracted folder. Upload **all 12 files below together** to the top level of your GitHub repository:

1. `index.html`
2. `404.html`
3. `privacy.html`
4. `thank-you.html`
5. `robots.txt`
6. `sitemap.xml`
7. `assets-01.zip`
8. `assets-02.zip`
9. `asset-manifest.json`
10. `build.py`
11. `netlify.toml`
12. `README.md`

Use a new empty GitHub repository for this new package. Choose **Add file → Upload files**, select these 12 files, then commit. The repository's main page should show `index.html`, `netlify.toml` and both assets ZIP files immediately. There should be no extra outer `blackshadesstudio` or `site` folder.

**Extract the outer download ZIP only. Keep `assets-01.zip` and `assets-02.zip` zipped when uploading them to GitHub.** Uploading only `index.html` will leave the photographs and styling unavailable.

## Netlify settings for THIS version

Import your new GitHub repository into Netlify. The included `netlify.toml` sets these automatically:

| Field | Value |
| --- | --- |
| Base directory | Leave empty (repository root) |
| Build command | `python3 build.py` |
| Publish directory | `dist` |
| Environment variables | None required |

If an old manual setting says `site`, change it to `dist` for this package. A build command is required for this version; it unpacks the photos/styles and checks every file. No pip or npm installation is required by the website.

Deploy and wait for a successful build. The log should contain:

`Build passed: all 134 portfolio photographs and 286 asset files verified.`

Then open the live `.netlify.app` address and check the photos, styling, mobile menu and image viewer. Keep your existing domain DNS pointing to the same Netlify site if reconnecting this repository to it. A newly created Netlify site has its own `.netlify.app` address, so its www CNAME target must use that new address.

## Local preview or manual Netlify upload

Run `python3 build.py` in this folder (on Windows, `python build.py` also works). Open `dist/index.html` for a local preview. To deploy manually, upload the generated **dist folder** to Netlify. Do not drag this unbuilt repository package into Netlify's manual deploy area: manual deployment does not run build commands.

## Enquiries

WhatsApp and phone: +971 54 484 0241. Email: blackshadesstudio@gmail.com.

The links are included. Netlify form delivery still requires enabling Forms detection, redeploying, and configuring notifications to your email address in Netlify. Test a real enquiry after deployment.

## What was checked

The same build command was run locally. It unpacks both archives and checks all asset hashes, HTML resource paths, CSS font references, section anchors and the 134-photo count. The generated pages and photographic assets match the previous completed website. Live Netlify deployment and browser/device interaction testing still need verification in your account.

## Update photos later

The archives contain the ordinary CSS, JavaScript, fonts and image files under `assets/`. Running the build restores that complete folder inside `dist`. If editing assets, regenerate the corresponding archive and `asset-manifest.json` together; the build deliberately rejects mismatched files.

Official references:
- https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository
- https://docs.netlify.com/build/configure-builds/overview/
- https://docs.netlify.com/build/configure-builds/manage-dependencies/
