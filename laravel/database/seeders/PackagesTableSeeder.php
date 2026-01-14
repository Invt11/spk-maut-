<?php
namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class PackagesTableSeeder extends Seeder
{
    public function run()
    {
        DB::table('packages')->insert([
            [
                'code' => 'A',
                'name' => 'Bangkok–Pattaya',
                'destination' => 'Thailand',
                'duration' => 5,
                'price' => 10300000,
                'facilities' => 'Hotel, tiket PP, transport, driver/guide',
                'rating' => 4.0,
                'created_at' => now(), 'updated_at' => now(),
            ],
            [
                'code' => 'B',
                'name' => 'Holiday in Singapore',
                'destination' => 'Singapore',
                'duration' => 4,
                'price' => 5800000,
                'facilities' => 'Hotel, tiket PP, transport, driver/guide',
                'rating' => 4.6,
                'created_at' => now(), 'updated_at' => now(),
            ],
            [
                'code' => 'C',
                'name' => 'Taiwan Hsinchu Tour',
                'destination' => 'Taiwan',
                'duration' => 7,
                'price' => 18000000,
                'facilities' => 'Hotel, tiket PP, transport, driver/guide',
                'rating' => 4.3,
                'created_at' => now(), 'updated_at' => now(),
            ],
            [
                'code' => 'D',
                'name' => 'Explore Korea Alpaca',
                'destination' => 'Korea Selatan',
                'duration' => 8,
                'price' => 18800000,
                'facilities' => 'Hotel, tiket PP, transport, driver/guide',
                'rating' => 4.4,
                'created_at' => now(), 'updated_at' => now(),
            ],
            [
                'code' => 'E',
                'name' => 'Paket Tour China 2025',
                'destination' => 'China',
                'duration' => 7,
                'price' => 15500000,
                'facilities' => 'Hotel, tiket PP, transport, driver/guide',
                'rating' => 4.2,
                'created_at' => now(), 'updated_at' => now(),
            ],
        ]);
    }
}
