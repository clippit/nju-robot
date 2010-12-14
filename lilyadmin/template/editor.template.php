<?php header ( "content-type:text/html;charset=utf-8" ); ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
	<title>慧聚南大</title>
	<link rel="stylesheet" type="text/css" media="screen" href="js/datePicker.css" />
	<script type="text/javascript" src='ckeditor/ckeditor.js'></script>
	<script type="text/javascript" src='ckfinder/ckfinder.js'></script>
	<link rel="stylesheet" type="text/css" media="screen" href="js/datePicker.css">
	
	<link rel="stylesheet" href="css/ui-lightness/jquery-ui-1.8.6.custom.css">
	<link rel="stylesheet" href="css/validationEngine.jquery.css">
	<link rel="stylesheet" href="css/template.css">
	<link rel="stylesheet" href="css/editor.css">
	<script src="js/jquery.js"></script>
	<script src="js/jquery-1.4.2.min.js"></script>	
	<script src="js/jquery-ui-1.8.6.custom.min.js"></script>	
	<script type="text/javascript" src="js/jquery.validationEngine-fr.js"></script>
	<script type="text/javascript" src="js/jquery.validationEngine.js"></script>
	<script  type="text/javascript">
		$(function() {
			$( "#accordion" ).accordion();
			date = new Date();
			str  = date.getFullYear() + "-" + (date.getMonth()+1)+ "-" + date.getDate();
			var strDate=str;
			
			$('#datepicker').datepicker({
				inline: true,
//				autoSize: true,
				dateFormat: 'yy-mm-dd',
				minDate: strDate,
				firstDay: strDate
			});
		});
	</script>
</head>
<body>
<?php 
$view_value = $this->values; 
	
$modify = !empty($this->values['post']);
if($modify){
	
	$post = $this->values['post'];
}
?>
<div id="wrapper_bg">
	<div class="wrapper">
		<div class="header">
			<img id="logo" src="imgs/logo.png" />
			<h1 id="site_name">智汇南大</h1>
			<a id="logout" href="index.php?action=logout">注销登录&gt;&gt;</a>
		</div>
		<div class="main">
			<?php if($this->messages){?>
			<div id="messages" >
			<ul>
			<?php foreach ($this->messages as $value) { ?>
				<li><?php echo '&nbsp;&nbsp;'.$value;?></li>
			<?php }?>
			</ul>
			</div>
			<?php }?>
			<form action="index.php?action=save" method="post">
			<div class="editor_header">
				<span class="item"><span class="label">活动标题:</span><input tabindex="1" class="validate[required] text-input" type="text" id="post_title" name="title" value="<?php if($modify){echo stripcslashes($post['post_title']);}?>"  /></span>
				<div class="clear"></div>
				<span id="time_wrapper" class="item">
					<span class="label">讲座时间:</span>
					<span id="time_picker">
                    <?php 
					if($modify){
						list($date, $time) = explode(" ", $post['coming_date']);
						list($y, $m, $d) = explode("-", $date);
						list($h, $min) = explode(":", $time);
					}
					?>
						<select name="year">
						<?php for($i = date('Y'); $i < date('Y') + 3; $i++){?>
							<option <?php if($modify){if($y == $i){echo 'selected="selected"';}}  ?>><?php echo $i?></option>
						<?php }?>
						</select>
						年
						<select name="month">
						<?php for($i = 1; $i < 13; $i++){?>
							<option <?php if($modify){if($m == $i){echo 'selected="selected"';}}  ?>><?php echo str_pad($i, 2, "0", STR_PAD_LEFT);?></option>
						<?php }?>
						</select>
						月
						<select name="day">
						<?php for($i = 1; $i < 32; $i++){?>
							<option <?php if($modify){if($d == $i){echo 'selected="selected"';}}  ?>><?php echo str_pad($i, 2, "0", STR_PAD_LEFT);?></option>
						<?php }?>
						</select>
						日
						<select name="hour">
						<?php for($i = 0; $i < 24; $i++){?>
							<option <?php if($modify){if($h == $i){echo 'selected="selected"';}}  ?>><?php echo str_pad($i, 2, "0", STR_PAD_LEFT);?></option>
						<?php }?>
						</select>
						时
						<select  name="min">
						<?php for($i = 0; $i < 60; $i++){?>
							<option <?php if($modify){if($min == $i){echo 'selected="selected"';}}  ?>><?php echo str_pad($i, 2, "0", STR_PAD_LEFT);?></option>
						<?php }?>
						</select>分
					</span>
				</span>
				<div class="clear"></div>
				<span id="place_wrapper" class="item"><span class="label">讲座地点:</span><input tabindex="2" class="validate[required] text-input"  type="text" id="place" name="place" value="<?php if($modify){echo stripcslashes($post['place']);}?>" /> </span>
				<div class="clear"></div>
				<span class="item"><span class="label">主讲人:</span><input tabindex="4" class="validate[required] text-input"  type="text" id="speakers" name="speakers" value="<?php if($modify){echo stripcslashes($post['speakers']);}?>"  /> </span>
				<div class="clear"></div>
				<span class="item"><span class="label">关键词:</span><input tabindex="5" class="text-input"  type="text" id="keywords" name="keywords" value="<?php if($modify){if($post['keywords']){echo $post['keywords'];}else{echo '多关键词用分号分开';};}else{ echo '多关键词用分号分开';}?>" onClick="javascript:if(this.value==='多关键词用分号分开'){this.value='';}" onBlur="javascript:if(this.value === ''){this.value='多关键词用分号分开'}" /> </span>
                <div class="clear"></div>
                <span class="item"><span class="label">文章类型:</span>
               
                <select name="type" id="type_picker">
                <?php global $types; foreach($types as $index=>$value){  ?>
                    <option value="<?php echo $index;?>" <?php if($modify){ if($index == $post['type']){echo 'selected="selected"';}}  ?>><?php  echo $value; ?></option>
                <?php }?>
                </select>
           		</span>
				<div class="clear"></div>
				<span class="item" id='optrations'><span class="label">讲座简介:</span>
                <span  id="operation">
				<input tabindex="7" type="button" onClick="javascript:self.location='index.php'" value="新文章" name="publish" id="publish"  />
				<input tabindex="6" type="submit" value="<?php if($modify){echo '更新';}else{echo '发表';};?>" name="publish" id="publish"  /></span></span>
			</div>
			<div class="clear"></div>
			<div class="edit_body">
					<div class='input'>
						<textarea tabindex="5" class="validate[required] text-input" rows='80' cols='100' id="editor1" name="content" >
						<?php if($modify){echo $post['post_content'];}?>
						</textarea> 
						<script type="text/javascript">
							// Replace the <textarea id="editor1"> with an CKEditor instance.
							var smiles = new Array();
							for (var i = 1; i <= 37; i++) {
								smiles.push(i.toString() + '.gif');
							}
							var editor = CKEDITOR.replace('editor1', {
								toolbar: [['Source','Bold', 'Italic','Cut', 'Copy', 'Paste', 'PasteText','Bold','Italic', 'Underline', 'Strike'], ['Styles', 'Font', 'FontSize'], ['TextColor', 'BGColor', 'Smiley','Link', 'Unlink','Image','Flash','Table','HorizontalRule','PageBreak']],
								//toobar:'Basic',
								height: 350,
								width:695,
								filebrowserBrowseUrl : 'ckfinder/ckfinder.html',
								filebrowserImageBrowseUrl : 'ckfinder/ckfinder.html?Type=Images',
								filebrowserFlashBrowseUrl : 'ckfinder/ckfinder.html?Type=Flash',
								filebrowserUploadUrl : 'ckfinder/core/connector/php/connector.php?command=QuickUpload&type=Files',
								filebrowserImageUploadUrl : 'ckfinder/core/connector/php/connector.php?command=QuickUpload&type=Images',
								filebrowserFlashUploadUrl : 'ckfinder/core/connector/php/connector.php?command=QuickUpload&type=Flash',
						        filebrowserImageWindowWidth : '800',
						        filebrowserImageWindowHeight : '600',
								uiColor : '#efefef',
								resize_enabled: false,
								enterMode: 2,
								shiftEnterMode: 2,
								language: 'zh-cn',
								smiley_path: 'ckeditor/plugins/smiley/xn_images/',
								// filebrowserWindowWidth 
								smiley_images: smiles,
								font_defaultLabel: '宋体',
								fontSize_defaultLabel: '16',
								font_names: '宋体;楷体;隶书;华文行楷;黑体;微软雅黑;幼圆;Arial;Times New Roman;Verdana'
								});
							CKFinder.SetupCKEditor(editor, 'ckfinder/'); //ckfinder总目录的相对路径.
							//							extraPlugins : 'autogrow',
						</script>
					</div>
					<input type="hidden" name="submitted" value="1">
					<?php if($modify){?>
					
					<input type="hidden" id="pid" name="pid" value="<?php echo $post['pid']?>" />
					<input type="hidden" id="modify" name="modify" value="1" />
					
					<?php }?>
				</div>
			</form>
		</div>
		
		<div id="sidebar">
		<h3>最近编辑文章</h3>
			<div id="post_list">
				<?php if($this->recent_posts){
					$recent_posts = $this->recent_posts;
				?>
				<table  border="0" cellspacing="0" cellpadding="0">
					<?php foreach ($recent_posts as $recent_post) {
						?>
						<tr>
							<td>
								<a class="post_title" title="点击查看" href="index.php?action=edit&pid=<?php echo $recent_post['pid']?>"><?php echo $recent_post['post_title']; ?></a>&nbsp;&nbsp;
							</td>
							<td>
								<a class="modify" href="index.php?action=edit&pid=<?php echo $recent_post['pid']?>">修改</a>
							</td>
							<td>
								<a class="delete" onClick="javascript:if(confirm('确定要删除这篇文章吗？')){ return true;}else{return false;}" href='index.php?action=delete&pid=<?php echo $recent_post['pid']?>'>删除</a>
							</td>
						</tr>
					<?php }?>
				<?php ?>
				</table>
				<?php
				}
				?>
			</div>
		</div>
		<div class="clear"></div>
		<div id="footer">
			<div id="copyright">Copyright@2010 powered by <a href="http://www.lilystudio.org">LilyStudio</a></div>
		</div>
	</div> 
</div>
</body>
</html>