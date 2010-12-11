<?php
include_once 'View.class.php';
class LoginView extends View{
	var $values = array();
	/* (non-PHPdoc)
	 * @see View::__construct()
	 */
	public function __construct() {
		// TODO Auto-generated method stub
		
	}

	/* (non-PHPdoc)
	 * @see View::display()
	 */
	public function display() {
		include_once '/../template/login.template.php';
	}
/* (non-PHPdoc)
	 * @see View::auth()
	 */
	function auth() {
		// TODO Auto-generated method stub
		
	}


	
}