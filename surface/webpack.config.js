const path = require('path');
const combineLoaders = require('webpack-combine-loaders');

const APP_DIR = path.resolve(__dirname, 'src');
const DIST = path.resolve(__dirname, 'dist');

module.exports = {
	entry: `${APP_DIR}/index.js`,
	output: {
		path: DIST,
		publicPath: '/dist/',
		filename: '[name].js'
	},
	target: 'electron-renderer',
	module: {
		rules: [
			{
				test: /\.(js|jsx)$/,
				include: APP_DIR,
				exclude: /node_modules/,
				use: {
					loader: 'babel-loader'
				}
			},
			{
				test: /\.css$/,
				loader: combineLoaders([
					{ loader: 'style-loader' },
					{loader: 'css-loader' }
				])
			}
		]},
	performance: { hints: false }
};