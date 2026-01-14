<?php
namespace App\Console\Commands;

use Illuminate\Console\Command;
use App\Models\Package;
use App\Services\MautService;

class RunMaut extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'maut:run {--export= : export to csv (csv)}';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Run MAUT on packages from the database and optionally export results';

    public function handle()
    {
        $this->info('Running MAUT on packages table...');

        $packages = Package::all();
        if ($packages->isEmpty()) {
            $this->warn('No packages found in packages table.');
            return 1;
        }

        $data = [];
        foreach ($packages as $p) {
            $data[] = [
                'Alternative' => $p->name,
                'Price' => (float) $p->price,
                'Duration' => (int) $p->duration,
                'Facilities' => 4, // placeholder: parse `facilities` if needed
                'Destination' => 4.0, // placeholder: map destination to numeric score if needed
                'Rating' => $p->rating ?? 4.0,
            ];
        }

        $criteria = ['Price', 'Duration', 'Facilities', 'Destination', 'Rating'];
        $weights = [
            'Price' => 0.25,
            'Duration' => 0.15,
            'Facilities' => 0.20,
            'Destination' => 0.20,
            'Rating' => 0.20,
        ];
        $benefit = [
            'Price' => false,
            'Duration' => false,
            'Facilities' => true,
            'Destination' => true,
            'Rating' => true,
        ];

        $maut = new MautService();
        $results = $maut->maut($data, $criteria, $weights, $benefit);

        $rows = [];
        foreach ($results as $i => $r) {
            $rows[] = [
                $i + 1,
                $r['Alternative'],
                number_format($r['Price'], 0, ',', '.'),
                $r['Duration'],
                $r['Rating'],
                number_format($r['Score'], 6)
            ];
        }

        $this->table(['Rank','Alternative','Price','Duration','Rating','Score'], $rows);

        $export = $this->option('export');
        if ($export === 'csv') {
            $path = storage_path('app/maut_results.csv');
            $fp = fopen($path, 'w');
            fputcsv($fp, ['Rank','Alternative','Price','Duration','Facilities','Destination','Rating','Score']);
            foreach ($results as $i => $r) {
                fputcsv($fp, [$i+1, $r['Alternative'], $r['Price'], $r['Duration'], $r['Facilities'], $r['Destination'], $r['Rating'], $r['Score']]);
            }
            fclose($fp);
            $this->info('Exported results to: ' . $path);
        }

        return 0;
    }
}
