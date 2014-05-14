<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh-CN" lang="zh-CN">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" >
  <title>知乎寻人</title>
</head>
<body>
	<div id="head">
	<form action="/name" method="GET">
	<input type="text" name="keyword" maxlength="100"> 
	<input type="submit" value="Go">
	</form>
	<div id="head">

		<div id="peoples">
			%for p in peoples:
				<li><a href={{"http://www.zhihu.com"+p}} target=_blank>{{p}}</a></li>
			%end
		</div>
</body>
</html>
