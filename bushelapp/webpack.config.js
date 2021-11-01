const webpack = require('webpack');
module.exports = function(_env, argv) {
	const isProd = argv.mode == 'production';


	return {
		devtool: isProd ? false : 'source-map',
		entry:  ["regenerator-runtime/runtime.js", __dirname + '/react/edit.js'],
		output: {
			path: __dirname + '/static/scripts',
			filename: 'editbundle.js',
			publicPath: '/static/scripts/',
		},
		resolve: {
			extensions: ['.js', '.jsx']
		},

		module: {
			rules: [
				{
				test: /\.(js|jsx)?/,
					exclude: /node_modules/,
					use: {
						loader: 'babel-loader',
						options: {
							cacheDirectory: true,
							cacheCompression: false,
							envName: isProd ? 'production' : 'development',
						}
					}	
				}	
			]
		}
	};
};