<!-- edit.blade.php -->
@if ($errors->any())
    <div class="alert alert-danger">
        <ul>
            @foreach ($errors->all() as $error)
                <li>{{ $error }}</li>
            @endforeach
        </ul>
    </div>
@endif


@extends('layouts.app')

@section('content')
<header style="background-color: #66cdaa;">
</header>
<body style="background-color: #dcdcdc;">
<div class="container">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card">
                <div class="card-header" style="background-color: #e6e6fa;">{{ __('スケジュール編集') }}</div>

                <div class="card-body" style="background-color: #e6e6fa;">
                    <form action="{{ route('schedules.update', $schedule->id) }}" style="background-color: #e6e6fa;" style="background-color: #f0f8ff;" method="POST">
                        @csrf
                        @method('PUT') <!-- 更新メソッド指定 -->
                        
                        <div class="mb-3" style="background-color: #e6e6fa;">
                            <label for="title" class="form-label">タイトル:</label>
                            <input type="text" class="form-control" style="background-color: #f0f8ff;" name="title" value="{{ old('title', $schedule->title) }}" required>
                        </div>

                        <div class="mb-3" style="background-color: #e6e6fa;">
                            <label for="description" class="form-label">説明:</label>
                            <textarea class="form-control" style="background-color: #f0f8ff;" name="description">{{ old('description', $schedule->description) }}</textarea>
                        </div>

                        <div class="mb-3" style="background-color: #e6e6fa;">
                            <label for="start_time" class="form-label">開始時間:</label>
                            <input type="datetime-local" class="form-control" style="background-color: #f0f8ff;" name="start_time" value="{{ old('start_time', \Carbon\Carbon::parse($schedule->start_time)->format('Y-m-d\TH:i')) }}" required>
                        </div>

                        <div class="mb-3" style="background-color: #e6e6fa;">
                            <label for="end_time" class="form-label">終了時間:</label>
                            <input type="datetime-local" class="form-control" style="background-color: #f0f8ff;" name="end_time" value="{{ old('end_time', \Carbon\Carbon::parse($schedule->end_time)->format('Y-m-d\TH:i')) }}" required>
                        </div>

                        <button type="submit" class="btn btn-primary">更新</button>
                    </form>
                    
                    <div class="mt-3" style="background-color: #e6e6fa;">
                        <!-- 削除ボタン -->
                        <form action="{{ route('schedules.destroy', $schedule->id) }}" style="background-color: #f0f8ff;" method="POST" class="d-inline">
                            @csrf
                            @method('DELETE')
                            <button type="submit" class="btn btn-danger"
                                onclick="return confirm('本当に削除しますか？')">削除</button>
                        </form>
                    </div>

                    <div class="mt-3" style="background-color: #e6e6fa;">
                        <a href="{{ route('schedules') }}" class="btn btn-secondary me-2">戻る</a>
                        <a href="{{ route('dashboard') }}" class="btn btn-outline-primary">{{ __('ダッシュボードへ戻る') }}</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
@endsection


