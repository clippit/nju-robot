<?php
$path=dirname(__FILE__);
include_once $path.'/View.class.php';
include_once $path.'/../db/db.php';
class EditorView extends View {
	var $values = array ();
	/* (non-PHPdoc)
	 * @see View::display()
	 */
	public function display() {
		if ($this->auth ()) {
			include_once dirname(__FILE__).'/../template/editor.template.php';
		} else {
			$login_view = new LoginView ();
			$login_view->display ();
		}
	}
	/* (non-PHPdoc)
	 * @see View::__construct()
	 */
	public function __construct() {
		// TODO Auto-generated method stub
		$db = new DB();
		$this->recent_posts = $db->get_recent_posts($_SESSION['uid'], 10);
	}
	
	/* (non-PHPdoc)
	 * @see View::auth()
	 */
	public function auth() {
		// TODO Auto-generated method stub
		return true;
	}

}