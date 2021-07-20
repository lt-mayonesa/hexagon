# Changelog

<!--next-version-placeholder-->

## v0.13.5 (2021-07-20)
### Fix
* **execute:** Use subprocess shell=True ([#38](https://github.com/redbeestudios/hexagon/issues/38)) ([`6d5e1e8`](https://github.com/redbeestudios/hexagon/commit/6d5e1e8e2e6ce62ca15acbf9d002d3ae6d0881ef))

## v0.13.4 (2021-07-19)
### Fix
* **yaml:** Handle error for None values ([`33300c6`](https://github.com/redbeestudios/hexagon/commit/33300c6463ab7f0accdccf0b46ed7fb96be64ac4))

## v0.13.3 (2021-07-17)
### Fix
* Simplify always true cli.command ([`c72de85`](https://github.com/redbeestudios/hexagon/commit/c72de855b7f8a0e236a9ea100d0e2662f8d90895))

## v0.13.2 (2021-07-17)
### Fix
* **last-command:** Store last command whe tool executed directly ([`1f6c887`](https://github.com/redbeestudios/hexagon/commit/1f6c8875317245b599b18063420650277d9d27b8))

## v0.13.1 (2021-07-13)
### Fix
* **help:** Help expecting dict crashes ([`cf86f99`](https://github.com/redbeestudios/hexagon/commit/cf86f99c56e9c5a4affe426021b3230ef342d99f))

## v0.13.0 (2021-07-13)
### Feature
* **yaml:** Show a more precise error to users ([#27](https://github.com/redbeestudios/hexagon/issues/27)) ([`b635964`](https://github.com/redbeestudios/hexagon/commit/b635964789a54006f3f3b4dc31196940487b687f))

## v0.12.0 (2021-07-12)
### Feature
* Define tools & envs as lists ([#26](https://github.com/redbeestudios/hexagon/issues/26)) ([`4db03b4`](https://github.com/redbeestudios/hexagon/commit/4db03b4e279bf2c82f6c9e8af8265026ea6e25c6))

## v0.11.0 (2021-07-10)
### Feature
* **domain:** Map YAML to pydantic BaseModel ([#24](https://github.com/redbeestudios/hexagon/issues/24)) ([`727a09a`](https://github.com/redbeestudios/hexagon/commit/727a09a01f11c34b1225fdcab609b02b2ffbff09))

## v0.10.0 (2021-07-08)
### Feature
* **execute:** Command actions, closes #22 ([#23](https://github.com/redbeestudios/hexagon/issues/23)) ([`26a9e05`](https://github.com/redbeestudios/hexagon/commit/26a9e051b497354c55177398f95ef98b0b4149bb))

## v0.9.0 (2021-07-07)
### Feature
* **support:** Storage api, closes #17 ([#21](https://github.com/redbeestudios/hexagon/issues/21)) ([`f8cc5b3`](https://github.com/redbeestudios/hexagon/commit/f8cc5b374df56c084c2b1cc48ba0a35c44c6a46e))

## v0.8.2 (2021-07-03)
### Fix
* **execute:** Pass env object correctly ([`86bbc68`](https://github.com/redbeestudios/hexagon/commit/86bbc689001339f0bfc128b25520244ed7f966ec))

## v0.8.1 (2021-07-02)


## v0.8.0 (2021-07-01)
### Feature
* **styles:** Basic support for hexagon themes ([#14](https://github.com/redbeestudios/hexagon/issues/14)) ([`b5dd966`](https://github.com/redbeestudios/hexagon/commit/b5dd966a221cab477e33adec27fb54fdfc6efefb))

### Documentation
* English, slogan, and reference to template repo ([`9a9fc96`](https://github.com/redbeestudios/hexagon/commit/9a9fc96f42d4ea81a57bda822de7c098d31015a6))

## v0.7.6 (2021-06-25)
### Fix
* **create-tool:** __templates dir and custom tools path ([#9](https://github.com/redbeestudios/hexagon/issues/9)) ([`5ebde69`](https://github.com/redbeestudios/hexagon/commit/5ebde697b840e5da0ea62341ef22831ecc53a50d))

## v0.7.5 (2021-06-25)
### Fix
* **save-alias:** Bash on fresh install ([#8](https://github.com/redbeestudios/hexagon/issues/8)) ([`1754d2c`](https://github.com/redbeestudios/hexagon/commit/1754d2c02fde3231a142bc2fa51c344eef390e37))

## v0.7.4 (2021-06-23)
### Fix
* **create-tool:** Templates directory not published ([`0f1e85c`](https://github.com/redbeestudios/hexagon/commit/0f1e85c45969d1f1f5cd7ab9dbb0b4018f9a8243))

## v0.7.3 (2021-06-22)
### Fix
* **tracer:** Do not print alias for internal tools ([`5d798fe`](https://github.com/redbeestudios/hexagon/commit/5d798fe1d49b12b36bcf74decc1765468c888422))

## v0.7.2 (2021-06-19)
### Fix
* **save-alias:** Create aliases file if does not exist ([`9055055`](https://github.com/redbeestudios/hexagon/commit/9055055c8def45fc1b84c5b13388be50e259f86a))

### Documentation
* Yaml example in readme ([`86c28d1`](https://github.com/redbeestudios/hexagon/commit/86c28d126535e3fb6cd229b623666666aa0e1bd3))

## v0.7.1 (2021-06-17)
### Fix
* **execute:** Run install_cli and other internal tools ([#2](https://github.com/redbeestudios/hexagon/issues/2)) ([`71cc90b`](https://github.com/redbeestudios/hexagon/commit/71cc90b9493332825f78163854422db5d2ec493d))

## v0.7.0 (2021-06-17)
### Feature
* **execute:** Execute action with extension ([`fe622a8`](https://github.com/redbeestudios/hexagon/commit/fe622a8942d91eb3c2f5c9cbe88d1aac22f1ea0f))

## v0.6.0 (2021-06-16)
### Feature
* **internal-tools:** Create a new tool ([`dfc13aa`](https://github.com/redbeestudios/hexagon/commit/dfc13aacf77ec17ba735a519dd4bfbce29047731))

### Fix
* **wax:** Make classifier optional ([`4e8ff5b`](https://github.com/redbeestudios/hexagon/commit/4e8ff5bce035883b49a21f062c4a543529983f69))
* **create-tool:** Change ordering of YAML key insert ([`1ce6024`](https://github.com/redbeestudios/hexagon/commit/1ce6024b06f6b6cfbf0b0af8db6d6703a79efd35))
* **help:** Support tools with no long_name ([`46c0f89`](https://github.com/redbeestudios/hexagon/commit/46c0f896dfb63288b3662b8d08499c6c66998b47))
* **wax:** Show classifier when no long_name ([`bc8a485`](https://github.com/redbeestudios/hexagon/commit/bc8a485ced377d6ddd78ae7617a6fc1f6d2ad889))
* **execute:** Fail with custom message when action not found ([`5ea46f2`](https://github.com/redbeestudios/hexagon/commit/5ea46f21aa69dfd5de615d67ac823034b6854ac4))

## v0.5.0 (2021-06-12)
### Feature
* **config:** Only show install cli when no config ([`9413f99`](https://github.com/redbeestudios/hexagon/commit/9413f99ffa23f562f68acddfe99c73e817e74e3e))

### Fix
* Allow for tools with no alias ([`eb25e89`](https://github.com/redbeestudios/hexagon/commit/eb25e8976581bc9f39852b93444c91b6a074210f))

## v0.4.1 (2021-06-11)
### Fix
* **install:** Wrong action definition for tool install ([`425dfd3`](https://github.com/redbeestudios/hexagon/commit/425dfd349da6c60361ef69839752126632c67bd7))

## v0.4.0 (2021-06-11)
### Feature
* **config:** Custom tools dir relative to YAML ([`fe3e26b`](https://github.com/redbeestudios/hexagon/commit/fe3e26bd3598ece02e9fd06ae4397b14edce6947))

## v0.3.0 (2021-06-11)
### Feature
* **prompt:** Sort tools by type ([`ef71eae`](https://github.com/redbeestudios/hexagon/commit/ef71eae1e2b5bb0b7b996efa5a1c694b52f31235))
* **custom-tool:** Allow projects to register custom tools ([`1cac9ca`](https://github.com/redbeestudios/hexagon/commit/1cac9ca80e369f9c05c1dcc3363386d4af0d6828))

### Documentation
* **release:** Correct regex for README version ([`f9b973a`](https://github.com/redbeestudios/hexagon/commit/f9b973a514efc0370a32d5b95a515ed461a508c2))

## v0.2.0 (2021-06-10)
### Feature
* Handle keyboard interrupt gracefully ([`a65daa2`](https://github.com/redbeestudios/hexagon/commit/a65daa26c3de305a2bacafe7f7a64f9295914c94))
* **install:** Install custom cli from YAML ([`cb25d68`](https://github.com/redbeestudios/hexagon/commit/cb25d680fa2af6448a79e61631542dabc08991a9))

### Documentation
* Basic readme content ([`7a82b34`](https://github.com/redbeestudios/hexagon/commit/7a82b3490f2b112c9a35fad4a789de1d2341ad69))

## v0.1.0 (2021-06-06)
### Feature
* **envs:** Make tool.envs optional ([`efeec06`](https://github.com/redbeestudios/hexagon/commit/efeec064404830ca33c6b4751f55455190c6b9e2))

## v0.0.6 (2021-06-06)
### Fix
* **help:** Optional alias ([`3cf1f6a`](https://github.com/redbeestudios/hexagon/commit/3cf1f6a46276468fc7a9ae5bbb4445ff4f544d11))

### Documentation
* **release:** Version update comment ([`c6a9617`](https://github.com/redbeestudios/hexagon/commit/c6a9617e7943adef2095b1a768548c8692cefd67))
