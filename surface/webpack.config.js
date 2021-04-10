const HtmlWebpackPlugin = require('html-webpack-plugin');
const path = require('path');

module.exports = [
    {
      mode: 'development',
      entry: './main.ts',
      target: 'electron-main',
      module: {
        rules: [{
          test: /\.ts$|tsx/,
          include: __dirname,
          use: {
            loader: 'ts-loader'
          }
        }]
      },
      output: {
        path: __dirname + '/dist',
        filename: 'electron.js'
      },
      resolve: {
        extensions: ['.ts', '.js', '.tsx'],
        alias: {
          log: __dirname + '/src/components/Log'
        }
      }
    },
    {
        mode: 'development',
        entry: './src/index.tsx',
        target: 'electron-renderer',
        devtool: 'source-map',
        module: { 
            rules: [{
                test: /\.(ts|tsx)$/,
                include: /src/,
                exclude: /node_modules/,
                use: {
                  loader: 'ts-loader'
                }
            },
            {
                test: /\.s[ac]ss$/i,
                use: [
                    "style-loader",
                    "css-loader",
                    "sass-loader",
                ],
            }
        ] },
        node: {
            __dirname: true
        },
        output: {
          path: __dirname + '/dist',
          filename: '[name].js'
        },
        plugins: [
          new HtmlWebpackPlugin({
            template: './src/index.html'
          })
        ],
        resolve: {
            extensions: ['.js', '.ts', '.tsx', '.jsx', '.json'],
            mainFields: ['main', 'module', 'browser'],
            alias: {
              log: __dirname + '/src/components/Log'
            }
        }
      }
];