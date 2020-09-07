/**
 * Emoji class
 * @description http://as3coder.blogspot.com/2014/08/emoji.html
 * @author AS3Coder
 */
(function(){
/**
 * Define public access
 * @private
 */
var emoji = window.emoji = {};
emoji.replace = Replace;
/**
 * Grouping by range
 * @constant
 * @private
 */
var GROUPS =
  [
   [/(\ud83c[\udde8-\uddfa])(\ud83c[\udde7-\uddfa])/g, ReplaceFlags],     // Flags
   [/[\u0023-\u0039]\u20E3/g,                          ReplaceNumbers],   // Numbers
   [/[\u2139-\u3299]/g,                                ReplaceStandard],  // Unsorted
   [/[\u203C\u2049]/g,                                 ReplaceStandard],  // Punctuation
   [/([\ud800-\udbff])([\udc00-\udfff])/g,             ReplaceSurrogate]  // Other (surrogate pairs)
  ];
/**
 * Method to replace all emoji characters in the icon
 * @param {String} Source string
 * @return {String}
 * @public
 */
function Replace (source)
  {
   var pattern;
   //---
   for(var i=0, j=GROUPS.length; i<j; i++)
     {
      pattern = GROUPS[i];
      if(pattern && pattern[0] && pattern[1])
        {
         if(source.match(pattern[0]))
           {
            source = source.replace(pattern[0], pattern[1]);
           }
        }
     }
   //---
   return(source);
  }
/**
 * Method to replace flags
 * @return {String}
 * @private
 */
function ReplaceFlags (match)
  {
   return(GetHtmlCodeFromHex(
     [
      GetHexFromSurrogatePair(match.charCodeAt(0), match.charCodeAt(1)).toString(16),
      GetHexFromSurrogatePair(match.charCodeAt(2), match.charCodeAt(3)).toString(16)
     ].join('')));
  }
/**
 * Method to replace numbers
 * @return {String}
 * @private
 */
function ReplaceNumbers (match)
  {
   return(GetHtmlCodeFromHex(match.charCodeAt(0).toString(16) + match.charCodeAt(1).toString(16)));
  }
/**
 * Method to replace srandard charters
 * @return {String}
 * @private
 */
function ReplaceStandard (match)
  {
   return(GetHtmlCodeFromHex(match.charCodeAt(0).toString(16)));
  }
/**
 * Method to replace surrogate pairs
 * @return {String}
 * @private
 */
function ReplaceSurrogate (match, p1, p2)
  {
   return(GetHtmlCodeFromHex(GetHexFromSurrogatePair(p1.charCodeAt(0),p2.charCodeAt(0)).toString(16)));
  }
/**
 * The method returns the hex code for a surrogate pair
 * @return {String}
 * @private
 */
function GetHexFromSurrogatePair (a, b)
  {
   return((a - 0xD800) * 0x400 + (b - 0xDC00) + 0x10000);
  }
/**
 * The method returns an html code for icon image
 * @param {String} hex
 * @return {String}
 * @private
 */ 
function GetHtmlCodeFromHex (hex)
  {
   return(['<span class="emojic"><span class="emoji emoji', hex, '"></span><span class="emojit">&#x', hex, ';</span></span>'].join(''));
  }
//---
})();