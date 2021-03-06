/**
 * @license Copyright (c) 2003-2014, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.md or http://ckeditor.com/license
 */

CKEDITOR.editorConfig = function( config ) {
	//config.allowContent = true ('p' = <p> tag / default로 toolbar button이 있는 tag는 허용) 
	
//config.uiColor ='#CCEAEE';
	config.skin = 'bootstrapck';
	//Language setting
 	config.defaultLanguage = 'ko';
	config.language = 'ko';
	config.width = 600;
    config.height = 30;
	//autoGrow 
	//config.extraPlugins = 'autogrow';
	//config.autoGrow_minHeight = 300;
	//config.autoGrow_maxHeight = 600;
	//toolbar setting
	config.toolbar = [
		[ 'Cut', 'Copy', '-',],
		[ 'Bold','Italic','Underline','Strike','-','RemoveFormat' ],
	];
	
	
};
