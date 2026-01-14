<?php
namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Http\Controllers\Controller;
use App\Services\MautService;
use Illuminate\Support\Facades\Storage;

class MautController extends Controller
{
    protected $maut;

    public function __construct(MautService $maut)
    {
        $this->maut = $maut;
    }

    public function index(Request $request)
    {
        // default criteria
        $criteria = ['Price', 'Duration', 'Facilities', 'Destination', 'Rating'];

        // default weights
        $weights = $request->input('weights', [
            'Price' => 0.25,
            'Duration' => 0.15,
            'Facilities' => 0.2,
            'Destination' => 0.2,
            'Rating' => 0.2,
        ]);

        // default benefit map
        $benefit = $request->input('benefit', [
            'Price' => false,
            'Duration' => false,
            'Facilities' => true,
            'Destination' => true,
            'Rating' => true,
        ]);

        // read CSV from storage/app/alternatives.csv if exists, else empty
        $rows = [];
        $path = storage_path('app/alternatives.csv');
        if (file_exists($path)) {
            if (($handle = fopen($path, 'r')) !== false) {
                $headers = fgetcsv($handle);
                while (($data = fgetcsv($handle)) !== false) {
                    $row = [];
                    foreach ($headers as $i => $h) {
                        $row[$h] = $data[$i] ?? null;
                    }
                    // normalize column names used in service
                    $rows[] = [
                        'Alternative' => $row['Alternative'] ?? $row['Nama Paket'] ?? '',
                        'Price' => isset($row['Price']) ? floatval($row['Price']) : (isset($row['Harga (Rp)']) ? floatval(str_replace(['.',','],['',''],$row['Harga (Rp)'])) : 0),
                        'Duration' => isset($row['Duration']) ? intval($row['Duration']) : (isset($row['Durasi (hari)']) ? intval($row['Durasi (hari)']) : 0),
                        'Facilities' => 4, // placeholder: in real app parse fasilitas string
                        'Destination' => isset($row['Destination']) ? 4.0 : 4.0,
                        'Rating' => isset($row['Rating']) ? floatval($row['Rating']) : 4.0,
                    ];
                }
                fclose($handle);
            }
        }

        $results = [];
        if (!empty($rows)) {
            $results = $this->maut->maut($rows, $criteria, $weights, $benefit);
        }

        return view('maut', [
            'results' => $results,
            'weights' => $weights,
            'benefit' => $benefit,
        ]);
    }
}
