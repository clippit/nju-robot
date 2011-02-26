<?php

abstract class View{
	abstract function __construct();
	abstract function auth();
	function display(){
		$this->auth();
	}
}