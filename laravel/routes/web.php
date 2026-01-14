<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\MautController;

Route::get('/maut', [MautController::class, 'index']);
