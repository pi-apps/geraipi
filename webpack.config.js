var path = require("path");
var BundleTracker = require("webpack-bundle-tracker");
const FileManagerPlugin = require('filemanager-webpack-plugin');

module.exports = {
  context: __dirname,
  entry: {
    main: "./assets/js/index",
    other: "./assets/js/other",
  },
  output: {
    path: path.resolve(__dirname, "static/webpack_bundles/"),
    publicPath: "auto",
    filename: "[name].js",
  },

  plugins: [
    new BundleTracker({ path: __dirname, filename: "webpack-stats.json" }),
    new FileManagerPlugin({
        events: {
            onEnd: {
              copy: [{
                source: './static/webpack_bundles/other.js',
                destination: './frontend/templates/firebase-messaging-sw.js',
              }],
            },
        }
    }),
  ],

  module: {
    rules: [
      // we pass the output from babel loader to react-hot loader
      {
        test: /\.jsx?$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
        },
      },
    ],
  },

  resolve: {
    extensions: [".js", ".jsx"],
  },
};