# Integrasi MAUT ke Laravel
 `laravel/README.md` — instruksi integrasi singkat

Tambah: migration, model, dan seeder untuk data paket telah ditambahkan pada folder `laravel/`.

Langkah untuk mengimpor data ke aplikasi Laravel Anda:

1. Salin folder `laravel/database/migrations/2026_01_14_000000_create_packages_table.php` ke `database/migrations/` di proyek Laravel Anda.
2. Salin `laravel/app/Models/Package.php` ke `app/Models/`.
3. Salin `laravel/database/seeders/PackagesTableSeeder.php` ke `database/seeders/`.
4. Pastikan koneksi database Anda dikonfigurasi di `.env`.
5. Jalankan migrasi dan seeder:

```bash
php artisan migrate
php artisan db:seed --class=PackagesTableSeeder
```

Setelah itu data paket akan tersimpan di tabel `packages` dan dapat diakses oleh controller contoh `MautController`.

Butuh saya juga buatkan:
 perintah Artisan (`php artisan maut:run`) untuk menjalankan dari CLI, atau
 parser otomatis fasilitas/destination saat seeding?

Artisan command

Contoh perintah Artisan ditambahkan: `maut:run`.

Cara pakai setelah Anda menyalin file ke aplikasi Laravel:

```bash
# jalankan maut dan tampilkan tabel hasil di console
php artisan maut:run

# jalankan maut dan ekspor hasil ke CSV (stored at storage/app/maut_results.csv)
php artisan maut:run --export=csv
```

Catatan: contoh command menggunakan `MautService` yang ada di `app/Services/` dan migrasi/seeder yang disertakan untuk mengisi tabel `packages`.
- `app/Http/Controllers/MautController.php` — controller yang membaca CSV, menerima bobot/tipe, menjalankan MAUT, dan mengirim hasil ke view.
- `app/Services/MautService.php` — logika MAUT (normalisasi, perhitungan skor).
- `routes/web.php` — rute contoh untuk menampilkan form dan hasil.
- `resources/views/maut.blade.php` — tampilan sederhana untuk input bobot dan menampilkan peringkat.

Cara pakai (di repo Laravel Anda):

1. Salin file `MautController.php` ke `app/Http/Controllers/`.
2. Salin file `MautService.php` ke `app/Services/`.
3. Tambahkan rute pada `routes/web.php` (atau gabungkan potongan rute yang disediakan).
4. Salin `maut.blade.php` ke `resources/views/`.
5. Tempatkan file CSV Anda di `storage/app/alternatives.csv` atau unggah melalui form.

Contoh: buka `/maut` di browser, atur bobot lalu klik "Run MAUT".
