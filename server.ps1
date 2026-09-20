# Lightweight PowerShell HTTP Server
# Run with: powershell -ExecutionPolicy Bypass -File server.ps1
param(
    [int]$Port = 8080
)

$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add("http://localhost:$Port/")
$listener.Prefixes.Add("http://127.0.0.1:$Port/")

try {
    $listener.Start()
    Write-Host "==========================================================" -ForegroundColor Green
    Write-Host " [ASCII TERMINAL PORTFOLIO] Local Server Active!" -ForegroundColor Cyan
    Write-Host " Serving at: http://localhost:$Port/" -ForegroundColor Yellow
    Write-Host " Press Ctrl+C to terminate server." -ForegroundColor Gray
    Write-Host "==========================================================" -ForegroundColor Green

    $basePath = $PSScriptRoot

    $mimeTypes = @{
        ".html" = "text/html; charset=utf-8"
        ".css"  = "text/css; charset=utf-8"
        ".js"   = "application/javascript; charset=utf-8"
        ".json" = "application/json; charset=utf-8"
        ".txt"  = "text/plain; charset=utf-8"
        ".svg"  = "image/svg+xml"
        ".png"  = "image/png"
        ".ico"  = "image/x-icon"
        ".mp4"  = "video/mp4"
    }

    while ($listener.IsListening) {
        try {
            $context = $listener.GetContext()
            $request = $context.Request
            $response = $context.Response

            $rawPath = $request.Url.LocalPath.TrimStart('/')
            if ([string]::IsNullOrEmpty($rawPath)) {
                $rawPath = "index.html"
            }

            $filePath = Join-Path $basePath $rawPath

            if (Test-Path $filePath -PathType Leaf) {
                $ext = [System.IO.Path]::GetExtension($filePath).ToLower()
                $contentType = "application/octet-stream"
                if ($mimeTypes.ContainsKey($ext)) {
                    $contentType = $mimeTypes[$ext]
                }

                $bytes = [System.IO.File]::ReadAllBytes($filePath)
                $response.ContentType = $contentType
                $response.ContentLength64 = $bytes.Length
                $response.StatusCode = 200
                if ($request.HttpMethod -ne "HEAD") {
                    $response.OutputStream.Write($bytes, 0, $bytes.Length)
                }
            } else {
                $response.StatusCode = 404
                $msg = [System.Text.Encoding]::UTF8.GetBytes("404 Not Found: $rawPath")
                $response.ContentType = "text/plain"
                $response.ContentLength64 = $msg.Length
                if ($request.HttpMethod -ne "HEAD") {
                    $response.OutputStream.Write($msg, 0, $msg.Length)
                }
            }

            $response.Close()
        } catch {
            Write-Host "Request error: $_" -ForegroundColor Red
        }
    }
} finally {
    $listener.Stop()
    $listener.Close()
}
