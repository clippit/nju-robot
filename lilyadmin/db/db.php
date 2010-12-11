<?php
include_once '/db_config.php';
class DB {
	var $post_cols = array ('post_title', 'post_content', 'public_date', 'coming_date', 'type', 'uid' );
	
	var $dbc;
	var $dbh = null;
	public function __construct() {
		$this->dbh = new PDO ( 'sqlite:' . SLQITE_DB );
	
	}
	private function inject_check($sql_str) {
		return eregi ( 'select|insert|update|delete|\'|\/\*|\*|\.\.\/|\.\/|order|by|and 1\=|union|into|load_file|outfile', $sql_str ); // 进行过滤
	}
	public function is_user_exist($uname, $pwd) {
		if (! $this->inject_check ( $uname ) && ! $this->inject_check ( $pwd )) {
			$sql = 'select * from users where uname="' . $uname . '" and pwd = "' . $pwd . '"';

			$this->dbh->beginTransaction ();
			$sth = $this->dbh->prepare ( $sql );
			$sth->execute ();
			$this->dbh->commit ();
			$result = $sth->fetchAll ();
			if (count ( $result ) == 1) {
				$arr = $result [0];
				return $arr ['uid'];
			} else {
				return - 1;
			}
		} else {
			return - 1;
		
		}
	}
	
	public function new_post($valueArr) {
		$sql = 'insert into posts(post_title, post_content, publish_date, coming_date, type, uid, place, speakers, statue, keywords) values(';
		$size = sizeof ( $valueArr );
		$i = 0;
		foreach ( $valueArr as $value ) {
			$sql .= "'$value'";
			$i ++;
			if ($i != $size) {
				$sql .= ' , ';
			}
		}
		
		$sql .= ')';
		
		$this->dbh->beginTransaction ();
		$sth = $this->dbh->prepare ( $sql );
		if ($sth->execute ()) {
			$this->dbh->commit ();
			return $this->dbh->lastInsertId (); // 		返回      pid
		} else {
			return - 1;
		}
	}
	
	public function update_post($values, $pid) {
		$sql = 'update posts set ';
		$size = count ( $values );
		$i = 0;
		$indexs = array_keys ( $values );
		for(; $i < $size - 1; $i ++) {
			$key = $indexs [$i];
			$sql .= " $key " . '=' . "'$values[$key]'" . ', ';
		}
		$sql .= " $indexs[$i]" . '=' . "'$values[$key]' ";
		@session_start ();
		
		$sql .= ' where uid = ' . $_SESSION ['uid'] . ' and ' . ' pid = ' . $pid;
		
		$this->dbh->beginTransaction ();
		$sth = $this->dbh->prepare ( $sql );
		
		if ($sth->execute ()) {
			$this->dbh->commit ();
			return true;
		} else {
			return false;
		}
	}
	
	public function get_post_by_id($id) {
		if (is_numeric ( $id )) {
			$sql = 'select * from posts where pid = ' . $id;
			$this->dbh->beginTransaction ();
			$sth = $this->dbh->prepare ( $sql );
			$sth->execute ();
			$this->dbh->commit ();
			$result = $sth->fetchAll ();
			if ($result) {
				return $result [0];
			} else {
				return null;
			}
		} else {
			return null;
		}
	}
	
	public function get_recent_posts($uid = 0, $count = 15) {
		if (is_numeric ( $uid ) && is_numeric ( $count )) {
			$sql = 'select pid, post_title from posts where statue = 1 and uid = ' . $uid . ' order by publish_date desc limit 0,' . $count;
		} else {
			return null;
		}
		$this->dbh->beginTransaction ();
		$sth = $this->dbh->prepare ( $sql );
		$sth->execute ();
		$result = $sth->fetchAll ();
		
		if ($result) {
			return $result;
		} else {
			return null;
		}
	}
	
	public function delete_post($pid) {
		if (is_numeric ( $pid )) {
			$sql = 'delete from posts where pid=' . $pid . ' and uid=' . $_SESSION ['uid'];
			$this->dbh->beginTransaction ();
			$sth = $this->dbh->prepare ( $sql );
			if ($sth->execute ()) {
				$this->dbh->commit ();
				return true;
			} else {
				return false;
			}
		} else {
			return false;
		}
	}
}
