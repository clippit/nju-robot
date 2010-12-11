<html>
	<head>
		<meta http-equiv="content-type" content="text/html; charset=utf-8" >
		<title>登陆</title>
		<link rel="stylesheet" type="text/css" media="screen" href="css/login.css">
	</head>
	<body>
	<div id="outer_wrapper">
		<div id="wrapper">
			<div id="login_header">
				<img src="imgs/logo.png" />
				<h1>慧聚南大</h1>
			</div>
			<?php if(isset($this->messages)){?>
			<div id="error_msg">
				<ul>
					<?php foreach ($this->messages as $message) {?>
						<li><?php echo $message; ?></li>
					<?php }?>
				</ul>
			</div>
			<?php }?>
			
			<form id="form" action="index.php?action=login" method="post">
				<div style="height:30px;width:100%;"></div>
				<div id="name_block" class="input_area">
					<label>用户名：</label>
					<div class="input_wrapper"><input type="text" id="name" name="uname" value="<?php if (isset($_GET['uname']) )echo $_GET['uname'];?>" /></div>
				</div>
				<div class="clear"></div>
				<div id="pwd_block" class="input_area">
					<label>密码：</label>
					<div class="input_wrapper"><input id="password" type="password" name="pwd"/></div>
				</div>
				<input type="hidden" name="submitted" value="1"/>
				<div class="clear"></div>
				<div class="input_area">
					<input id="login" type="submit" value="登&nbsp;&nbsp;&nbsp;录" />
				</div>
				<div id="copyright">Powered By <a href="http://www.lilystudio.org">LilyStudio</a></div>
			</form>
		</div>
	</div>
	</body>
	
</html>