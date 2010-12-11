<?php
include_once 'view/LoginView.class.php';
include_once 'view/EditorView.class.php';
include_once 'db/db.php';
include_once 'config.php';

if (! isset ( $_REQUEST ['action'] ) || empty ( $_REQUEST ['action'] )) { //default action 
	if (auth ()) { // if in to Editor
		$view = new EditorView ();
	} else { //not, to log in
		$view = new LoginView ();
	}
} else if ($_REQUEST ['action'] == 'login') {
	if (isset ( $_POST ['submitted'] )) { // request from form submit,   a valid login
		$user_name = $_POST ['uname'];
		$pwd = $_POST ['pwd'];
		$db = new DB ();
		$uid = $db->is_user_exist ( $user_name, $pwd );
		if ($uid > 0) {
			@session_start ();
			$_SESSION ['uid'] = $uid;
			$view = new EditorView ();
		} else {
			$view = new LoginView ();
			$view->messages [] = '账号或密码错误！';
		}
	} else { //request from address bar, invalid login, to Login page
		$view = new LoginView ();
	}
} else if ($_REQUEST ['action'] == 'save') { //create a new post
	if (auth ()) {
		if (isset ( $_POST ['submitted'] )) { //request from form submit, valid post submit;
			$post = request_post ();
			$db = new DB ();
			if (isset ( $_POST ['modify'] )) { // test if this is a modify to a old post, if it is, update post instead of create a new one.
				if ($db->update_post ( $post, $_REQUEST ['pid'] )) { //if it wants to update a old post, pid must be given.
					$view = new EditorView ();
					$view->messages [] = '更新文章成功';
					$post ['pid'] = $_REQUEST ['pid'];
				} else {
					$view = new EditorView ();
					$view->messages [] = '更新文章失败';
				}
			} else {
				$pid = $db->new_post ( $post );
				if ($pid > 0) {
					$view = new EditorView ();
					$view->messages [] = '文章保存成功';
					$post ['pid'] = $pid;
				} else {
					$view = new EditorView ();
					$view->messages [] = '文章保存失败';
				}
			}
			$view->values ['post'] = $post;
		} else { //if request come from the address bar, then go to Editor and do nothing
			$view = new EditorView ();
		}
	} else {
		$view = new LoginView ();
	}
} else if ($_REQUEST ['action'] == 'edit') { //prepare the required post to be edit
	if (auth ()) {
		if ($_REQUEST ['pid']) {
			$db = new DB ();
			$view = new EditorView ();
			$view->values ['post'] = $db->get_post_by_id ( $_REQUEST ['pid'] );
		} else {
			$view = new EditorView ();
		}
	} else {
		$view = new LoginView ();
	}
} else if ($_REQUEST ['action'] == 'delete') { //delete post
	if (auth ()) {
		$pid = $_REQUEST ['pid'];
		$db = new DB ();
		$del_restult = $db->delete_post ( $pid );
		$view = new EditorView ();
		if ($del_restult) {
			$view->messages [] = '文章删除成功！';
		} else {
			$view->messages [] = '文章删除失败！';
		}
	} else {
		$view = new LoginView ();
	}
} else if ($_REQUEST ['action'] == 'logout') {
	@session_start ();
	$view = new LoginView ();
	if (auth ()) {
		$_SESSION ['uid'] = '';
		$view->messages [] = '注销成功';
	} else {
		$view->messages [] = '您还未登录';
	}
} else {
	$view = new LoginView ();
}
if ($view) {
	$view->display ();
}

function auth() {
	//	return true;
	@session_start ();
	if (isset ( $_SESSION ['uid'] ) && (! empty ( $_SESSION ['uid'] ))) {
		return true;
	} else {
		return false;
	}
}
function request_post() {
	$post = array ();
	$post ['post_title'] = addslashes ( htmlspecialchars ( $_REQUEST ['title'] ) );
	$post ['post_content'] = addslashes ( htmlspecialchars ( $_REQUEST ['content'] ) );
	$post ['publish_date'] = date ( 'Y-m-d-G-i-s' );
	$post ['coming_date'] = addslashes ( $_REQUEST ['year'].'-'. $_REQUEST ['month'].'-'. $_REQUEST ['day'].'-'. $_REQUEST ['hour'].'-'. $_REQUEST ['min']);
	$post ['type'] = 1;
	$post ['uid'] = $_SESSION ['uid'];
	$post ['place'] = addslashes ( $_REQUEST ['place'] );
	$post ['speakers'] = addslashes ( $_REQUEST ['speakers'] );
	$post ['statue'] = 1;
	$post ['keywords'] = addslashes ( $_REQUEST ['keywords'] );
	if($post ['keywords'] == '多关键词用分号分开'){
		$post ['keywords'] = '';
	}
	return $post;
}