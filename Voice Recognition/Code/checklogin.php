<?php
$uid = $_POST['user'];
$pw = $_POST['pass'];

if($uid == 'admin' and $pw == 'smarthome')
{	
	session_start();
	$_SESSION['sid']=session_id();
	header("location:securepage.php");
}
else
	
{

header("location: index.html");
}
