<?php
/**
 * Get the image from Lily BBS and resize it (if too large), then make a cache
 * 
 * @author clippit
 */
if (! isset($_GET ['r'])) {
	exit('Need a parameter!');
}
define(CACHE_DIR, './lily_images/');
$url = base64_decode($_GET ['r']);

switch (strtolower(substr($url, - 3))) {
	case 'jpg' :
	case 'pge' :
	case '.jp' :
		$type = 'image/jpeg';
		break;
	case 'png' :
		$type = 'image/png';
		break;
	case 'gif' :
		$type = 'image/gif';
		break;
	default :
		$type = '';
}
header("Content-Type: $type");

if (preg_match('/^http:\/\/bbs\.nju\.edu\.cn/', $url)) {
	if (file_exists(get_filename($url))) { // cache hit!
		echo file_get_contents(get_filename($url));
		exit();
	} else { // resize it and save cache
		$filename = get_filename($url);
		$img_content = fetch_bbs_image($url);
		file_put_contents($filename, $img_content);
		smart_resize_image($filename, 550, 550, true);
		echo file_get_contents($filename);
		exit();
	}

} else { // images out of the BBS
	header("Location: $url");
	exit();
}

function get_filename($url) {
	return CACHE_DIR . str_replace('/', '-', substr($url, 27));
}

function fetch_bbs_image($url) {
	$curl = curl_init($url);
	curl_setopt($curl, CURLOPT_HEADER, FALSE);
	curl_setopt($curl, CURLOPT_RETURNTRANSFER, TRUE);
	curl_setopt($curl, CURLOPT_REFERER, 'http://bbs.nju.edu.cn');
	$re = curl_exec($curl);
	if (curl_errno($curl)) {
		return NULL;
	}
	return $re;
}

/**
 * Smart Image Resizing while Preserving Transparency With PHP and GD Library
 * 
 * @author Maxim Chernyak
 * @link http://mediumexposure.com/smart-image-resizing-while-preserving-transparency-php-and-gd-library/
 */
function smart_resize_image($file, $width = 0, $height = 0, $proportional = false, $output = 'file', $delete_original = true, $use_linux_commands = false) {
	if ($height <= 0 && $width <= 0) {
		return false;
	}
	
	$info = getimagesize($file);
	$image = '';
	
	$final_width = 0;
	$final_height = 0;
	list ( $width_old, $height_old ) = $info;
	
	if ($proportional) {
		if ($width == 0)
			$factor = $height / $height_old;
		elseif ($height == 0)
			$factor = $width / $width_old;
		else
			$factor = min($width / $width_old, $height / $height_old);
		
		$final_width = round($width_old * $factor);
		$final_height = round($height_old * $factor);
	
	} else {
		$final_width = ($width <= 0) ? $width_old : $width;
		$final_height = ($height <= 0) ? $height_old : $height;
	}
	
	switch ($info [2]) {
		case IMAGETYPE_GIF :
			$image = imagecreatefromgif($file);
			break;
		case IMAGETYPE_JPEG :
			$image = imagecreatefromjpeg($file);
			break;
		case IMAGETYPE_PNG :
			$image = imagecreatefrompng($file);
			break;
		default :
			return false;
	}
	
	$image_resized = imagecreatetruecolor($final_width, $final_height);
	
	if (($info [2] == IMAGETYPE_GIF) || ($info [2] == IMAGETYPE_PNG)) {
		$trnprt_indx = imagecolortransparent($image);
		
		// If we have a specific transparent color
		if ($trnprt_indx >= 0) {
			
			// Get the original image's transparent color's RGB values
			$trnprt_color = imagecolorsforindex($image, $trnprt_indx);
			
			// Allocate the same color in the new image resource
			$trnprt_indx = imagecolorallocate($image_resized, $trnprt_color ['red'], $trnprt_color ['green'], $trnprt_color ['blue']);
			
			// Completely fill the background of the new image with allocated color.
			imagefill($image_resized, 0, 0, $trnprt_indx);
			
			// Set the background color for new image to transparent
			imagecolortransparent($image_resized, $trnprt_indx);
		
		} // Always make a transparent background color for PNGs that don't have one allocated already
		elseif ($info [2] == IMAGETYPE_PNG) {
			
			// Turn off transparency blending (temporarily)
			imagealphablending($image_resized, false);
			
			// Create a new transparent color for image
			$color = imagecolorallocatealpha($image_resized, 0, 0, 0, 127);
			
			// Completely fill the background of the new image with allocated color.
			imagefill($image_resized, 0, 0, $color);
			
			// Restore transparency blending
			imagesavealpha($image_resized, true);
		}
	}
	
	imagecopyresampled($image_resized, $image, 0, 0, 0, 0, $final_width, $final_height, $width_old, $height_old);
	
	if ($delete_original) {
		if ($use_linux_commands)
			exec('rm ' . $file);
		else
			@unlink($file);
	}
	
	switch (strtolower($output)) {
		case 'browser' :
			$mime = image_type_to_mime_type($info [2]);
			header("Content-type: $mime");
			$output = NULL;
			break;
		case 'file' :
			$output = $file;
			break;
		case 'return' :
			return $image_resized;
			break;
		default :
			break;
	}
	
	switch ($info [2]) {
		case IMAGETYPE_GIF :
			imagegif($image_resized, $output);
			break;
		case IMAGETYPE_JPEG :
			imagejpeg($image_resized, $output);
			break;
		case IMAGETYPE_PNG :
			imagepng($image_resized, $output);
			break;
		default :
			return false;
	}
	
	return true;
}
?>