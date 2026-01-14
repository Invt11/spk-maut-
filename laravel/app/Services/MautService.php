<?php
namespace App\Services;

class MautService
{
    // Normalize values by criteria and benefit/cost
    public function normalize(array $data, array $criteria, array $benefit): array
    {
        $norm = $data;
        foreach ($criteria as $c) {
            $values = array_map(function ($row) use ($c) {
                return floatval($row[$c]);
            }, $data);

            $mn = min($values);
            $mx = max($values);
            foreach ($norm as $i => $row) {
                if ($mx == $mn) {
                    $norm[$i][$c] = 1.0;
                } else {
                    if ($benefit[$c]) {
                        $norm[$i][$c] = (floatval($row[$c]) - $mn) / ($mx - $mn);
                    } else {
                        $norm[$i][$c] = ($mx - floatval($row[$c])) / ($mx - $mn);
                    }
                }
            }
        }
        return $norm;
    }

    // Compute MAUT scores
    public function maut(array $data, array $criteria, array $weights, array $benefit): array
    {
        $norm = $this->normalize($data, $criteria, $benefit);
        $results = [];
        foreach ($norm as $i => $row) {
            $score = 0.0;
            foreach ($criteria as $c) {
                $w = isset($weights[$c]) ? floatval($weights[$c]) : 0.0;
                $score += floatval($row[$c]) * $w;
            }
            $results[] = array_merge($data[$i], ['Score' => $score]);
        }
        // sort desc by Score
        usort($results, function ($a, $b) {
            if ($a['Score'] == $b['Score']) return 0;
            return ($a['Score'] > $b['Score']) ? -1 : 1;
        });
        return $results;
    }
}
