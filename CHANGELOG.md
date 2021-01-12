# Change Log

## [0.0.9](https://github.com/Spredzy/lecm/tree/0.0.9) (2021-01-12)

[Full Changelog](https://github.com/Spredzy/lecm/compare/0.0.7...0.0.9)

**Merged pull requests:**

- Get the intermediate certificate whenever needed [\#64](https://github.com/Spredzy/lecm/pull/64) ([fcharlier](https://github.com/fcharlier))
- Certificate: Roll-out from X3 intermediate to R3 [\#63](https://github.com/Spredzy/lecm/pull/63) ([sbadia](https://github.com/sbadia))

## [0.0.7](https://github.com/Spredzy/lecm/tree/0.0.7) (2016-11-18)

[Full Changelog](https://github.com/Spredzy/lecm/compare/0.0.6...0.0.7)

**Merged pull requests:**

- Service reload: Optimize the way services are reloaded [\#52](https://github.com/Spredzy/lecm/pull/52) ([Spredzy](https://github.com/Spredzy))
- Display a flag showing if conf and cert are in sync [\#51](https://github.com/Spredzy/lecm/pull/51) ([Spredzy](https://github.com/Spredzy))
- Allow user to force regenerate/renew certificates [\#50](https://github.com/Spredzy/lecm/pull/50) ([Spredzy](https://github.com/Spredzy))
- Renew: Do not fail when no certificate has already been generated [\#47](https://github.com/Spredzy/lecm/pull/47) ([Spredzy](https://github.com/Spredzy))
- Fedora: Prepare for the release in Fedora [\#45](https://github.com/Spredzy/lecm/pull/45) ([Spredzy](https://github.com/Spredzy))

## [0.0.6](https://github.com/Spredzy/lecm/tree/0.0.6) (2016-11-09)
[Full Changelog](https://github.com/Spredzy/lecm/compare/0.0.5...0.0.6)

**Implemented enhancements:**

- doc: Added instal. documentation \(pypi/debian\) [\#37](https://github.com/Spredzy/lecm/pull/37) ([sbadia](https://github.com/sbadia))

**Merged pull requests:**

- 0.0.6: Prepare release [\#44](https://github.com/Spredzy/lecm/pull/44) ([Spredzy](https://github.com/Spredzy))
- Print USAGE message when no parameter has been passed [\#43](https://github.com/Spredzy/lecm/pull/43) ([Spredzy](https://github.com/Spredzy))
- certificates: Allow one to use Let's Encrypt staging API [\#42](https://github.com/Spredzy/lecm/pull/42) ([Spredzy](https://github.com/Spredzy))
- setup.py: Fix url and add Python 3.5 support [\#41](https://github.com/Spredzy/lecm/pull/41) ([Spredzy](https://github.com/Spredzy))
- Travis: Add check for Python 3.5 [\#39](https://github.com/Spredzy/lecm/pull/39) ([Spredzy](https://github.com/Spredzy))
- certificates: Allow one to reload multiple service [\#38](https://github.com/Spredzy/lecm/pull/38) ([Spredzy](https://github.com/Spredzy))
- Mistake in the alias statement [\#36](https://github.com/Spredzy/lecm/pull/36) ([albatros69](https://github.com/albatros69))

## [0.0.5](https://github.com/Spredzy/lecm/tree/0.0.5) (2016-10-20)
[Full Changelog](https://github.com/Spredzy/lecm/compare/0.0.4...0.0.5)

**Implemented enhancements:**

- doc: Added a manpage for lecm packages \(can be generated with pandoc\) [\#34](https://github.com/Spredzy/lecm/pull/34) ([sbadia](https://github.com/sbadia))
- packaging/debian: Move packaging, to Debian: https://anonscm.debian.org/git/letsencrypt//python-lecm.git [\#33](https://github.com/Spredzy/lecm/pull/33) ([sbadia](https://github.com/sbadia))
- Deb packaging [\#31](https://github.com/Spredzy/lecm/pull/31) ([sbadia](https://github.com/sbadia))

**Merged pull requests:**

- 0.0.5: Prepare release [\#35](https://github.com/Spredzy/lecm/pull/35) ([Spredzy](https://github.com/Spredzy))
- Packaging: Introduce spec file [\#30](https://github.com/Spredzy/lecm/pull/30) ([Spredzy](https://github.com/Spredzy))
- Service: reload only when an action had been taken [\#29](https://github.com/Spredzy/lecm/pull/29) ([Spredzy](https://github.com/Spredzy))
- Sample: Add more sample as a base example [\#28](https://github.com/Spredzy/lecm/pull/28) ([Spredzy](https://github.com/Spredzy))
- Service reload: Rely on certificate object rather than configuration [\#27](https://github.com/Spredzy/lecm/pull/27) ([Spredzy](https://github.com/Spredzy))
- README: Fix left over backup string from a copy/paste [\#26](https://github.com/Spredzy/lecm/pull/26) ([Spredzy](https://github.com/Spredzy))
- SELinux: Enforce proper context for generated directories [\#25](https://github.com/Spredzy/lecm/pull/25) ([Spredzy](https://github.com/Spredzy))
- Run the reload command only when necessary [\#24](https://github.com/Spredzy/lecm/pull/24) ([Spredzy](https://github.com/Spredzy))
- Certificate: create a default value for account\_key\_name variable [\#23](https://github.com/Spredzy/lecm/pull/23) ([Spredzy](https://github.com/Spredzy))

## [0.0.4](https://github.com/Spredzy/lecm/tree/0.0.4) (2016-08-01)
[Full Changelog](https://github.com/Spredzy/lecm/compare/0.0.3...0.0.4)

**Merged pull requests:**

- 0.0.4: Release [\#18](https://github.com/Spredzy/lecm/pull/18) ([Spredzy](https://github.com/Spredzy))
- Python3: Make lecm works on Python3 [\#17](https://github.com/Spredzy/lecm/pull/17) ([Spredzy](https://github.com/Spredzy))

## [0.0.3](https://github.com/Spredzy/lecm/tree/0.0.3) (2016-07-23)
[Full Changelog](https://github.com/Spredzy/lecm/compare/0.0.2...0.0.3)

**Merged pull requests:**

- 0.0.3: Release [\#16](https://github.com/Spredzy/lecm/pull/16) ([Spredzy](https://github.com/Spredzy))
- Add support for platforms using sysv [\#15](https://github.com/Spredzy/lecm/pull/15) ([Spredzy](https://github.com/Spredzy))
- Certificate: Fix missing defaults \(type, service\_name\) [\#14](https://github.com/Spredzy/lecm/pull/14) ([Spredzy](https://github.com/Spredzy))
- Do not clean filesystem before requesting certs [\#13](https://github.com/Spredzy/lecm/pull/13) ([Spredzy](https://github.com/Spredzy))
- Avoid race condition when renewing certificates [\#12](https://github.com/Spredzy/lecm/pull/12) ([Spredzy](https://github.com/Spredzy))

## [0.0.2](https://github.com/Spredzy/lecm/tree/0.0.2) (2016-07-08)
**Merged pull requests:**

- 0.0.2: Release [\#11](https://github.com/Spredzy/lecm/pull/11) ([Spredzy](https://github.com/Spredzy))
- Fixes: Various fixes [\#10](https://github.com/Spredzy/lecm/pull/10) ([Spredzy](https://github.com/Spredzy))
- Private Key: Create the file with the proper permission [\#9](https://github.com/Spredzy/lecm/pull/9) ([Spredzy](https://github.com/Spredzy))
- cli: Add the --noop feature [\#8](https://github.com/Spredzy/lecm/pull/8) ([Spredzy](https://github.com/Spredzy))
- cli: Add the --items feature that limit scope of the action [\#7](https://github.com/Spredzy/lecm/pull/7) ([Spredzy](https://github.com/Spredzy))
- README: Move from .md to .rst [\#6](https://github.com/Spredzy/lecm/pull/6) ([Spredzy](https://github.com/Spredzy))
- QA: Initial commit with pep8 tests [\#5](https://github.com/Spredzy/lecm/pull/5) ([Spredzy](https://github.com/Spredzy))
- QA: Include .travis.yml file [\#4](https://github.com/Spredzy/lecm/pull/4) ([Spredzy](https://github.com/Spredzy))
- LE: Handle the case when Let's Encrypt does not return a certificate … [\#3](https://github.com/Spredzy/lecm/pull/3) ([Spredzy](https://github.com/Spredzy))
- logging: Allow debug level to be specified on the cli [\#2](https://github.com/Spredzy/lecm/pull/2) ([Spredzy](https://github.com/Spredzy))
- logging: Manage to write logging messages [\#1](https://github.com/Spredzy/lecm/pull/1) ([Spredzy](https://github.com/Spredzy))



\* *This Change Log was automatically generated by [github_changelog_generator](https://github.com/skywinder/Github-Changelog-Generator)*
