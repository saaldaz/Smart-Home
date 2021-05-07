<?php



if ((isset($_POST['dev1on'])) || (isset($_POST['dev1off'])))
{
	$file1 = "relay1.txt";
	$handle1 = fopen($file1,'w+');
	if (isset($_POST['dev1on']))
	{
	$onstring = "ON";
	fwrite($handle1,$onstring);
	fclose($handle1);
	header('Location: securepage.php');
	}
	else if(isset($_POST['dev1off']))
	{
	$offstring = "OFF";
	fwrite($handle1, $offstring);
	fclose($handle1);
	header('Location: securepage.php');
	}
}


elseif((isset($_POST['dev2on'])) || (isset($_POST['dev2off'])))
{
	$file2 = "relay2.txt";
	$handle2 = fopen($file2,'w+');
	

	if(isset($_POST['dev2on']))
	{
	$onstring = "ON";
	fwrite($handle2, $onstring);
	fclose($handle2);
	header('Location: securepage.php');
	}
	else if(isset($_POST['dev2off']))
	{
	$offstring = "OFF";
	fwrite($handle2, $offstring);
	fclose($handle2);
	header('Location: securepage.php');
	}
}


elseif ((isset($_POST['dev3on'])) || (isset($_POST['dev3off'])))
{
		$file1 = "relay3.txt";
		$handle1 = fopen($file1,'w+');
		if (isset($_POST['dev3on']))
		{
		$onstring = "ON";
		fwrite($handle1,$onstring);
		fclose($handle1);
		header('Location: securepage.php');
		}
		else if(isset($_POST['dev3off']))
		{
		$offstring = "OFF";
		fwrite($handle1, $offstring);
		fclose($handle1);
		header('Location: securepage.php');
		}
}


elseif ((isset($_POST['dev4on'])) || (isset($_POST['dev4off'])))
{
	$file1 = "relay4.txt";
	$handle1 = fopen($file1,'w+');
	if (isset($_POST['dev4on']))
	{
	$onstring = "ON";
	fwrite($handle1,$onstring);
	fclose($handle1);
	header('Location: securepage.php');
	}
	else if(isset($_POST['dev4off']))
	{
	$offstring = "OFF";
	fwrite($handle1, $offstring);
	fclose($handle1);
	header('Location: securepage.php');
	}
}




?>