# Changelog

## [0.10.0](https://github.com/alrodsa/saibyo/compare/v0.9.0...v0.10.0) (2025-07-08)


### Features

* new merge to develop from main ([1f151cb](https://github.com/alrodsa/saibyo/commit/1f151cbc83d7eb18b497071da13bdf440d94c2a7))


### Documentation

* Documentation added ([76260ac](https://github.com/alrodsa/saibyo/commit/76260ac0748a57de60cb4b493d46bc1ab1834534))

## [0.9.0](https://github.com/alrodsa/saibyo/compare/v0.8.0...v0.9.0) (2025-06-01)


### Features

* add check to ensure wheel exists before upload ([f3ec417](https://github.com/alrodsa/saibyo/commit/f3ec4179a05c1dc744c799174c73efc25b4eff03))
* add installation of Google Cloud SDK in Dockerfile ([8c34fd6](https://github.com/alrodsa/saibyo/commit/8c34fd6b1909f846307494ca750b7bf1f83b220f))
* configure .pypirc for GCP Artifact Registry and update upload command ([dee5568](https://github.com/alrodsa/saibyo/commit/dee556871143454459d36809b3b91b72640f6d41))
* update publish workflow for improved clarity and GCP authentication. ([cbe4898](https://github.com/alrodsa/saibyo/commit/cbe4898af861f321ccadb2d4d6c8ed611105dcb4))


### Bug Fixes

* add 'build' to publish dependencies in pyproject.toml ([108355b](https://github.com/alrodsa/saibyo/commit/108355b58f6c235b25f6905995b4566fefb7de27))
* add missing command to decode GCP service account key in publish workflow ([63dc505](https://github.com/alrodsa/saibyo/commit/63dc50503b71ad57993f31c8fb9d7a9428cae26e))
* add missing id for authentication step in publish workflow ([cf6bb94](https://github.com/alrodsa/saibyo/commit/cf6bb94b1849556c3edd948e73d5996be296f962))
* correct command for decoding GCP service account key and improve output clarity ([442d488](https://github.com/alrodsa/saibyo/commit/442d488f43f12eb8ab863cf11d3e14b249e696f4))
* correct import statement for version extraction in publish workflow ([680e8c9](https://github.com/alrodsa/saibyo/commit/680e8c92bb4f0786316e6565dad805b45441ab80))
* enhance publish workflow by improving virtual environment setup and version extraction process ([4bb2701](https://github.com/alrodsa/saibyo/commit/4bb27013bace4e73998cc8929356af38c51ab149))
* remove redundant Google Cloud authentication step in publish workflow ([e809c9f](https://github.com/alrodsa/saibyo/commit/e809c9f3f0debee4929d71c31001fc886a679083))
* simplify GCP service account key decoding and authentication steps ([0f3fe70](https://github.com/alrodsa/saibyo/commit/0f3fe70015c1333872750cb8d19085ddbdc84757))
* streamline publish workflow by removing unnecessary dependencies and updating version extraction method ([024669f](https://github.com/alrodsa/saibyo/commit/024669f722bd9df8d08c7dd855d38fc0e3ef5ab0))
* streamline Python environment activation and commands in publish workflow ([25d3507](https://github.com/alrodsa/saibyo/commit/25d3507bf9f73b541e68508376910c3cae2c1695))
* update default value for num_workers in InterpolatorConf and enhance output folder handling in Interpolator ([9c54c0c](https://github.com/alrodsa/saibyo/commit/9c54c0c348ed14a4a810fb5871beb6793715bbe9))
* update GCP Artifact Registry upload step to use twine and correct version extraction method ([b1001cc](https://github.com/alrodsa/saibyo/commit/b1001ccf5e30e8120ce512793222b1527cf9502f))
* update publish workflow to use Workload Identity Federation for GCP authentication and enhance upload command ([ed86439](https://github.com/alrodsa/saibyo/commit/ed8643942dec266f1853f68afcd31f0d10cf6d84))
* update Python commands to use virtual environment explicitly in publish workflow. ([2deb349](https://github.com/alrodsa/saibyo/commit/2deb349d91808f191589ad7d68e4ef23ce705ae7))
* update version extraction in publish workflow to use tomli and add tomli as a dependency ([2d75601](https://github.com/alrodsa/saibyo/commit/2d75601bcdca234fa80ebed8d4af98df828dbe97))


### Documentation

* added documentation ([1656e80](https://github.com/alrodsa/saibyo/commit/1656e80ea6394c759f38244999fbc68e97fa18e8))
* added documentation ([1656e80](https://github.com/alrodsa/saibyo/commit/1656e80ea6394c759f38244999fbc68e97fa18e8))
* enhance README with detailed library overview, configuration methods, and usage examples ([2d28b01](https://github.com/alrodsa/saibyo/commit/2d28b010bf49e26e8bb966a0ebd5535819fda5ff))
* update README for improved clarity and formatting ([5dcab69](https://github.com/alrodsa/saibyo/commit/5dcab6938aad2491c1a0ef49491655206f550bf1))
* update README to include detailed Table of Contents for improved navigation ([a7b1e9d](https://github.com/alrodsa/saibyo/commit/a7b1e9d2f3e80055863d4b958a575809c2c9f748))

## [0.8.0](https://github.com/alrodsa/saibyo/compare/v0.7.0...v0.8.0) (2025-05-23)


### Features

* enhance publish workflow to include GCP Artifact Registry upload. ([0170c9c](https://github.com/alrodsa/saibyo/commit/0170c9c93cdf853de4f819b3245f07e56a773f3e))
* enhance publish workflow to include GCP Artifact Registry upload. ([0170c9c](https://github.com/alrodsa/saibyo/commit/0170c9c93cdf853de4f819b3245f07e56a773f3e))
* enhance publish workflow to include GCP Artifact Registry upload. ([0a07502](https://github.com/alrodsa/saibyo/commit/0a07502c42eedac4914c350e9401a06976a3d85c))
* update publish workflow to correct virtual environment setup commands ([8d1e5fe](https://github.com/alrodsa/saibyo/commit/8d1e5fe41c62da17957921ab05313a1fa7a3ec75))
* update publish workflow to create and activate virtual environment. ([daa9702](https://github.com/alrodsa/saibyo/commit/daa97026890728a5cde97d7cdea9054eea654e5b))
* update publish workflow to use 'uv' for installing dependencies in virtual environment ([40dfc04](https://github.com/alrodsa/saibyo/commit/40dfc04368e01ca463e84da397f73cd333eb511f))
* update publish workflow to use virtual environment for dependency installation and version extraction. ([bef9f15](https://github.com/alrodsa/saibyo/commit/bef9f15db350cfb74f3ac2b509a2a97be4542c0f))

## [0.7.0](https://github.com/alrodsa/saibyo/compare/v0.6.1...v0.7.0) (2025-05-23)


### Features

* Adapted project to uv package manager. ([7c8c6b3](https://github.com/alrodsa/saibyo/commit/7c8c6b3c891afd748f36811d42e72747d22b0889))
* alrodsa change project manager ([a215969](https://github.com/alrodsa/saibyo/commit/a215969c829dbb3b88b321cc55c08fc0bf3e28a3))
* Enhance GitHub workflows with emoji labels for better readability. ([11a50c3](https://github.com/alrodsa/saibyo/commit/11a50c36b9d7aafb6be085610b2e1f1293f187fc))
* Update GitHub workflows to use uv package manager and enhance step descriptions. ([5eb13a3](https://github.com/alrodsa/saibyo/commit/5eb13a35b9781616f45acaf87bdf7abaeb4bcae5))
* Update publish workflow to install publish dependencies and refine optional dependencies in pyproject.toml. ([1aa7828](https://github.com/alrodsa/saibyo/commit/1aa782888ff8ac068e30eb6a8b6d8fce9c72d61b))
* Update Python CI workflow to install dev dependencies with --system flag. ([db34f1c](https://github.com/alrodsa/saibyo/commit/db34f1c796fb8ed5d2f659d02a4b27fe7ccb440c))
* Update Python CI workflow with improved step descriptions and virtual environment setup. ([9c45c14](https://github.com/alrodsa/saibyo/commit/9c45c147eb98ee6e8f32c8ef0ecdca45d8cf4840))

## [0.6.1](https://github.com/alrodsa/saibyo/compare/v0.6.0...v0.6.1) (2025-05-07)


### Bug Fixes

* correct file opening mode in version extraction script. ([dbd530e](https://github.com/alrodsa/saibyo/commit/dbd530ec5744d4a71a6154d4454b9b63ceeafb71))
* Fix publish workflow ([5cf5737](https://github.com/alrodsa/saibyo/commit/5cf573762b1c16a75d7289ac02c5e2564c670c11))
* Hotfix in publish workflow ([51afb1a](https://github.com/alrodsa/saibyo/commit/51afb1afd737b0010d832fdf084153255f8e4092))
* update file path for Flownet weights in publish workflow. ([4915edf](https://github.com/alrodsa/saibyo/commit/4915edff13602b5c94f2cdb6df0e212fa4f9bc34))

## [0.6.0](https://github.com/alrodsa/saibyo/compare/v0.5.0...v0.6.0) (2025-05-07)


### Features

* update GitHub Actions workflow to publish package to GitHub Releases ([99abec9](https://github.com/alrodsa/saibyo/commit/99abec92630c5fda475fe8b3947eb69f5b53ef65))
* update GitHub Actions workflow to publish package to GitHub Releases ([c8bc14c](https://github.com/alrodsa/saibyo/commit/c8bc14c2e962120f4bd0c75180f78484b9ee9951))

## [0.5.0](https://github.com/alrodsa/saibyo/compare/v0.4.0...v0.5.0) (2025-05-04)


### Features

* update GitHub Actions workflow for Saibyo package publishing ([7a75867](https://github.com/alrodsa/saibyo/commit/7a758670777fe2d15dc7d61ded45ce20538fdc82))
* update GitHub Actions workflow for Saibyo package publishing ([c585737](https://github.com/alrodsa/saibyo/commit/c585737ff9e5bab805e0bd446643842555eeab89))

## [0.4.0](https://github.com/alrodsa/saibyo/compare/v0.3.0...v0.4.0) (2025-05-04)


### Features

* include flownet.pkl in package data for weights module ([f1ccf03](https://github.com/alrodsa/saibyo/commit/f1ccf03dad421a0a1271bf1ad9b55add80a011b3))
* include flownet.pkl in package data for weights module ([f1ccf03](https://github.com/alrodsa/saibyo/commit/f1ccf03dad421a0a1271bf1ad9b55add80a011b3))
* include flownet.pkl in package data for weights module ([9cdec15](https://github.com/alrodsa/saibyo/commit/9cdec154cae379503c1163b7031b9c7477f4f747))

## [0.3.0](https://github.com/alrodsa/saibyo/compare/v0.2.1...v0.3.0) (2025-05-04)


### Features

* add weights module initialization file ([5a46252](https://github.com/alrodsa/saibyo/commit/5a46252543ec2bde1d70b9f61171541febf3c395))
* add weights module initialization file ([fa586bd](https://github.com/alrodsa/saibyo/commit/fa586bdb48ebc2d5012cbdb9d9b8c73dbca3f0d7))


### Bug Fixes

* update publish workflow to target Test PyPI instead of GitHub Package ([f79e342](https://github.com/alrodsa/saibyo/commit/f79e3429c82ff3f72b91212d862ccf09028c317e))
* update publish workflow to target Test PyPI instead of GitHub Package ([f79e342](https://github.com/alrodsa/saibyo/commit/f79e3429c82ff3f72b91212d862ccf09028c317e))

## [0.2.1](https://github.com/alrodsa/saibyo/compare/v0.2.0...v0.2.1) (2025-05-04)


### Bug Fixes

* update publish workflow to trigger on closed pull requests ([7a1499b](https://github.com/alrodsa/saibyo/commit/7a1499b21bd45f0e3f1400ddf6c521889dcdebe7))
* update publish workflow to trigger on closed pull requests ([7a1499b](https://github.com/alrodsa/saibyo/commit/7a1499b21bd45f0e3f1400ddf6c521889dcdebe7))

## [0.2.0](https://github.com/alrodsa/saibyo/compare/v0.1.0...v0.2.0) (2025-05-03)


### Features

* add dev dependency group for twine ([3d22d4c](https://github.com/alrodsa/saibyo/commit/3d22d4c7b802fc81c0ea34beb8703d5ed2df6f89))
* add initial __init__.py files for libs and base modules ([833895d](https://github.com/alrodsa/saibyo/commit/833895d5991beb919659e4350744a263176a9003))
* add initial implementation of saibyo library with core modules and CLI ([7d921b5](https://github.com/alrodsa/saibyo/commit/7d921b581f434068ea45ccea5471155ddf77779a))
* add initial release-please manifest configuration ([bbf59bd](https://github.com/alrodsa/saibyo/commit/bbf59bdd911c091edcc138a0fdc9ee7ad4dbf1d8))
* add logging configuration and initial log files ([585d9e7](https://github.com/alrodsa/saibyo/commit/585d9e79522ed6b1c8f380c8fe2eeb152e055395))
* add pull request template and semantic PR title check workflow ([3de81a2](https://github.com/alrodsa/saibyo/commit/3de81a28a91672b562b8da5003c64e86354fdd2c))
* implement configuration management for application settings ([862ec2c](https://github.com/alrodsa/saibyo/commit/862ec2ca4e1c20234579dba703ffe16e2aba8166))
* initialize saibyo package and add core functionality ([32678fc](https://github.com/alrodsa/saibyo/commit/32678fca5328900be9215fc3ef548d4d7a441167))
* update release-please configuration and remove obsolete config file ([667e325](https://github.com/alrodsa/saibyo/commit/667e3259c95c76418a20fabdc915cec4906bf6bc))

## 0.1.0 (2025-04-29)


### Features

* Added versioning ([9599321](https://github.com/alrodsa/saibyo/commit/9599321ccecf78abe638331351df78f2ae2d443e))
* **all:** Implementation of the whole interpolation flow. ([6b448ee](https://github.com/alrodsa/saibyo/commit/6b448ee0901eb6e9ec8e1dad082852be176ca5e6))
* **base:** Added base lib for the configuration of app. ([4d06ccc](https://github.com/alrodsa/saibyo/commit/4d06ccce7d53c8d9cf82c78197cde54b609d18d7))
* **ci:** Add GitHub Actions workflow for Python CI with PDM and coverage ([3aa0296](https://github.com/alrodsa/saibyo/commit/3aa029614f280f9111c951b36ddf8d27547838c9))
* **ci:** Add GitHub Actions workflow for Python CI with PDM and coverage reporting ([85601f8](https://github.com/alrodsa/saibyo/commit/85601f838e396d08783485aa83abb673b03f6101))
* **ci:** Enhance GitHub Actions workflow with linting and auto-fix steps ([63914f4](https://github.com/alrodsa/saibyo/commit/63914f403e07d1f20245f3bc32f81c0054be5e42))
* **cli:** Added cli command for interpolation. ([e558e73](https://github.com/alrodsa/saibyo/commit/e558e737e41dc2f2053beb82e02e8bd3437a26a1))
* **conf:** Added coniguration schema. ([909c1fd](https://github.com/alrodsa/saibyo/commit/909c1fda79fcf20cfae93d76e191d0415eb552ec))
* **constants:** Added constants for cli. ([8374060](https://github.com/alrodsa/saibyo/commit/8374060bad2100e5b4686a57df7377640c7f28a2))
* **logging:** Add logging configuration and logger implementation in libs/base/logs ([7d892ed](https://github.com/alrodsa/saibyo/commit/7d892edcf6131f58d4faafaf53d682feaf66783c))
* **release:** Add release-please workflow and configuration for vers… ([4f2c261](https://github.com/alrodsa/saibyo/commit/4f2c261d5344df999e5efa9d9f61ebcb9de84131))
* **release:** Add release-please workflow and configuration for versioning. ([874ba17](https://github.com/alrodsa/saibyo/commit/874ba172983f279a8f426261186a5f7333741745))
* **tests:** Add image generation utilities and update dev dependencies ([c461d63](https://github.com/alrodsa/saibyo/commit/c461d638dd80fc21d84eb20d3549eaed21e7c9ca))


### Documentation

* **all:** Add docstrings for interpolate function and Interpolator class, and FramePairDataset class. ([7bd51a4](https://github.com/alrodsa/saibyo/commit/7bd51a46c1d4bd15bd15436387f1cc65ba1dca96))
