# Insights 

This is a Markdown file to track my learnings & insights during the course of completing the various CS50W projects. 

## HTML, CSS 

1. Usage of `width: 100%`, `width: auto`.
   - `width: 100%` will make the content width 100%. Any margin, border, padding will be added to this width & the element will overflow its parent (if any of these are added).
   - `width: auto` will fit the element in the available space, including margin, border & padding. The remaining space after adjusting for margin, padding & border will be the available width/height.
   - `width: 100% + box-sizing: border box` will fit the element, including border & padding, in the available space except for margin.
   - [source](https://stackoverflow.com/a/48093702/15781733)

2. Aligning elements to the right
   - Elements can be aligned along a direction (left, right, top, bottom, etc.) by setting any of the following properties:
      - `float: right`
      - `margin-right: 0;`

3. Using `&nbsp` in `HTML` documents
   - `&nbsp` is actually one of the most frequently used HTML entities, it stands for **non-breaking space**, meaning that strings separated with this entity will not be separated and put into separate lines.
   - [source](https://mailtrap.io/blog/nbsp/#:~:text=is%20actually%20one%20of,and%20put%20into%20separate%20lines.)

4. Applying multiple stylesheets to a single `HTML` document
   - It is possible to apply multiple stylesheets to a single `HTML` document, although the downside of this is a slower performance of the webpage. 
   - Another thing to note is that the styles in the multiple stylesheets will be applied in the order that they are linked in the HTML document. In the following example, all the rules from style1.css would be applied first, then the rules from style2.css will be applied. This can cause similar rules to overwrite the rules from the previously linked files.
     ```html
     <link href="style1.css" rel="stylesheet">
     <link href="style2.css" rel="stylesheet">
     ...
     ```
   - [source](https://discuss.codecademy.com/t/can-you-apply-multiple-stylesheets-to-a-single-page/369792)

5. The `<body>` element may sometimes not cover the entire page, because another element that lies within the body may have issues.
   - [source](https://stackoverflow.com/questions/59547744/cannot-get-body-element-to-cover-entire-page)

6. Positioning an element at the center bottom of its parent div
   - ```css
      #somelement {
         position: absolute;
         left: 50%;
         bottom: 0px;
         -webkit-transform: translateX(-50%);
         transform: translateX(-50%)
      }
     ```
   - [source](https://stackoverflow.com/a/45968877/15781733)
