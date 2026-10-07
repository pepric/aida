<?php
/**
 * Chunked File Upload Processing Endpoint.
 *
 * Handles chunked data upload requests (e.g., via Plupload), combining binary parts
 * into target destination files within user temporary directory spaces.
 *
 * @package    AIDA
 * @subpackage Controllers\Upload
 * @author     Giuseppe Riccio
 * @version    1.1.0
 */
 
// (A) FUNCTION TO FORMULATE SERVER RESPONSE
/**
 * Formulate and output JSON response payload with HTTP status code.
 *
 * @param int    $ok   Success indicator flag (1 for success, 0 for error). Default 1.
 * @param string $info Explanatory response message or error detail. Default empty string.
 * @return void
 */
function verbose($ok=1,$info=""){
  // THROW A 400 ERROR ON FAILURE
  if ($ok==0) { http_response_code(400); }
  die(json_encode(["ok"=>$ok, "info"=>$info]));
}

// (B) INVALID UPLOAD
if (empty($_FILES) || $_FILES['file']['error']) {
  verbose(0, "Failed to move uploaded file.");
}

// (C) UPLOAD DESTINATION
// ! CHANGE FOLDER IF REQUIRED !
$user = $_POST["user"];
$filePath = isset($_POST["path"]) ? $_POST["path"] : __DIR__ . DIRECTORY_SEPARATOR . "users". DIRECTORY_SEPARATOR . $user ."/tmp";
//$filePath = __DIR__ . DIRECTORY_SEPARATOR . "users". DIRECTORY_SEPARATOR . $user ."/tmp";
if (!file_exists($filePath)) { 
  if (!mkdir($filePath, 0777, true)) {
    verbose(0, "Failed to create $filePath");
  }
}
$fileName = isset($_REQUEST["name"]) ? $_REQUEST["name"] : $_FILES["file"]["name"];
$filePath = $filePath . DIRECTORY_SEPARATOR . $fileName;

// (D) DEAL WITH CHUNKS
$chunk = isset($_REQUEST["chunk"]) ? intval($_REQUEST["chunk"]) : 0;
$chunks = isset($_REQUEST["chunks"]) ? intval($_REQUEST["chunks"]) : 0;
$out = @fopen("{$filePath}.part", $chunk == 0 ? "wb" : "ab");
if ($out) {
  $in = @fopen($_FILES['file']['tmp_name'], "rb");
  if ($in) {
    while ($buff = fread($in, 4096)) { fwrite($out, $buff); }
  } else {
    verbose(0, "Failed to open input stream");
  }
  @fclose($in);
  @fclose($out);
  @unlink($_FILES['file']['tmp_name']);
} else {
  verbose(0, "Failed to open output stream");
}

// (E) CHECK IF FILE HAS BEEN UPLOADED
if (!$chunks || $chunk == $chunks - 1) {
  rename("{$filePath}.part", $filePath);
}
verbose(1, "Upload OK");