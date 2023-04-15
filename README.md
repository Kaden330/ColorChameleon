# ColorChameleon

ColorChameleon is a command line tool that generates color names based on hex codes. It uses a database of pre-existing colors to find the closest match to the provided hex code and returns the corresponding color name. The tool uses the Delta E formula, as described in the paper "The CIE 2000 colour difference formula: CIEDE2000" by Ming Luo, to accurately calculate the difference between colors.

## How it Works
ColorChameleon compares the input hex code to the colors in the database and calculates the Delta E value for each one. The color with the smallest Delta E value is considered the closest match and its name is returned as the output.

## Usage
To use ColorChameleon, simply run the following command:

```$ bash color_name.sh "#B94E48"```

The input color must be in hex format and enclosed in quotes or the "#" symbol must be escaped. For example, the following command would also work:

```$ bash color_name.sh \#B94E48```

The script will download all the necessary packages automatically.

## Contributing
We welcome contributions to ColorChameleon! If you have any ideas for new features or enhancements, feel free to submit a pull request.

## License
ColorChameleon is released under the MIT License.
