<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>MAUT - Rodex Tours & Travel</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>body{padding:20px;}</style>
</head>
<body>
<div class="container">
    <h1>MAUT - Hasil Perankingan</h1>

    <form method="get" action="/maut">
        <div class="row">
            <div class="col-md-8">
                <p>Gunakan file CSV pada <code>storage/app/alternatives.csv</code>. Form untuk bobot belum aktif di contoh ini.</p>
            </div>
        </div>
        <button class="btn btn-primary">Run MAUT</button>
    </form>

    <hr>

    @if(!empty($results))
        <h3>Hasil</h3>
        <table class="table table-striped">
            <thead>
            <tr>
                <th>#</th>
                <th>Alternative</th>
                <th>Price</th>
                <th>Duration</th>
                <th>Facilities</th>
                <th>Destination</th>
                <th>Rating</th>
                <th>Score</th>
            </tr>
            </thead>
            <tbody>
            @foreach($results as $i => $r)
                <tr>
                    <td>{{ $i+1 }}</td>
                    <td>{{ $r['Alternative'] }}</td>
                    <td>{{ number_format($r['Price'],0,',','.') }}</td>
                    <td>{{ $r['Duration'] }}</td>
                    <td>{{ $r['Facilities'] }}</td>
                    <td>{{ $r['Destination'] }}</td>
                    <td>{{ $r['Rating'] }}</td>
                    <td>{{ number_format($r['Score'], 6) }}</td>
                </tr>
            @endforeach
            </tbody>
        </table>
    @else
        <p>Tidak ada data. Upload `alternatives.csv` ke `storage/app/` lalu jalankan kembali.</p>
    @endif
</div>
</body>
</html>
