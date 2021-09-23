const path = require('path');

module.exports = {
  // path to our input files (can be multiple)
  entry: {
    'add-edit-bundle': './assets/js/recAddEdit.js',
    'detail-bundle': './assets/js/recDetail.js',
  },
  output: {
    filename: '[name].js',  // output bundle file name (name will be the key from entry section)
    path: path.resolve(__dirname, './static/placerem/js'),  // path to our Django static directory
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        loader: "babel-loader",
        options: { presets: ["@babel/preset-env", "@babel/preset-react"] }
      },
      {
        test: /\.css$/i,
        use: ["style-loader", "css-loader"],
      },
      {
        test: /\.(png|jpg|gif)$/i,
        use: [
          {
            loader: 'url-loader',
            options: {
              limit: 8192,
            },
          },
        ],
      },
    ]
  }
};
