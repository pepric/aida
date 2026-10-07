<?php
 /**
 * CAPTCHA Image Generator Endpoint.
 *
 * Dynamically generates a PNG image containing a randomized alphanumeric CAPTCHA code,
 * applies visual noise (distorted rectangles, variable colors, and TTF font rotations),
 * and stores the generated verification string in the active user session.
 *
 * @package    AIDA
 * @subpackage Security
 * @author     Giuseppe Riccio
 * @version    1.1.0
 */
session_start();

/**
 * @var string $permitted_chars Alphanumeric character set used to build the CAPTCHA string.
 */
 $permitted_chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ';

/**
 * Generate a randomized string from a given character set.
 *
 * @param string $input    The set of allowed characters.
 * @param int    $strength The desired length of the generated string. Default 10.
 * @return string The randomized CAPTCHA string.
 */  
function generate_string($input, $strength = 10) {
    $input_length = strlen($input);
    $random_string = '';
    for($i = 0; $i < $strength; $i++) {
        $random_character = $input[mt_rand(0, $input_length - 1)];
        $random_string .= $random_character;
    }
  
    return $random_string;
}
/**
 * Initialize GD image canvas and configure visual noise/colors.
 */ 
$image = imagecreatetruecolor(200, 50);
 
imageantialias($image, true);
 
$colors = [];
 
$red = rand(125, 175);
$green = rand(125, 175);
$blue = rand(125, 175);
// Draw random background rectangles for visual noise 
for($i = 0; $i < 5; $i++) {
  $colors[] = imagecolorallocate($image, $red - 20*$i, $green - 20*$i, $blue - 20*$i);
}
 
imagefill($image, 0, 0, $colors[0]);
 
for($i = 0; $i < 10; $i++) {
  imagesetthickness($image, rand(2, 10));
  $line_color = $colors[rand(1, 4)];
  imagerectangle($image, rand(-10, 190), rand(-10, 10), rand(-10, 190), rand(40, 60), $line_color);
}
 
$black = imagecolorallocate($image, 0, 0, 0);
$white = imagecolorallocate($image, 255, 255, 255);
$textcolors = [$black, $white];

/**
 * Render CAPTCHA text on the canvas and store string in session.
 */ 
$fonts = [dirname(__FILE__).'/assets/fonts/Acme.ttf', dirname(__FILE__).'/assets/fonts/Ubuntu.ttf', dirname(__FILE__).'/assets/fonts/Merriweather.ttf', dirname(__FILE__).'/assets/fonts/PlayfairDisplay.ttf'];
$string_length = 6;
$captcha_string = generate_string($permitted_chars, $string_length);
 
$_SESSION['captcha_text'] = $captcha_string;
 
for($i = 0; $i < $string_length; $i++) {
  $letter_space = 170/$string_length;
  $initial = 15;
   
  imagettftext($image, 24, rand(-15, 15), $initial + $i*$letter_space, rand(25, 45), $textcolors[rand(0, 1)], $fonts[array_rand($fonts)], $captcha_string[$i]);
}
/**
 * Output PNG stream to client and destroy image resource.
 */ 
header('Content-type: image/png');
imagepng($image);
imagedestroy($image);
?>