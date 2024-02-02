# Habr Parser
![MIT License](https://img.shields.io/github/license/JustKappaMan/Habr-Parser)
![Code style: black](https://img.shields.io/badge/code%20style-black-black)

Parse info about the top articles on [Habr.com](https://habr.com) for a given period of time.

## How to Use
Install [dependencies](requirements.txt)

Either as script:
```shell
python3 -m habrparser [OPTION]...
```

Or as package:
```python
from habrparser import HabrParser

parser = HabrParser(period="alltime")
result = parser.run()
```

## Credits
Big thanks to:
* [JetBrains](https://www.jetbrains.com) for [Open Source Development license](https://www.jetbrains.com/community/opensource)

## License
This project is licensed under the MIT License.