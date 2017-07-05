# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/) and this project adheres to [Semantic Versioning]
(http://semver.org/).

## 0.5.1 - [Unreleased]
### Fixed
- bael - using "-g" will now generate graph if user will stop the application with CTRL+C
- pytest is not in the normal requiretments.
- fix PidIsNotRunning dependency - it was using old version of MorfDict.

## 0.5.0 - 2017-06-30
### Added
- this change log
- Task.run_before -> as a replacment for Task.build_if(RunTask)

### Fixed
- Documentation in some places.

### Changed
- Changed Task.add_dependency to Task.build_if.
- Changed AlwaysRebuild dependency name to AlwaysTrue.
