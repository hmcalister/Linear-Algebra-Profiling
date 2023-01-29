use clap::Parser;
use nalgebra::{SMatrix, SVector};
use rand::Rng;
use std::thread;

#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Number of trials to attempt
    #[arg(short, long, default_value_t = 100)]
    trials: usize,

    /// Number of multiplications per trial
    #[arg(short, long, default_value_t = 100)]
    multiplications: usize,

    /// Number of threads to use,
    /// Should divide number of trials evenly
    #[arg(long, default_value_t = 1)]
    threads: usize,
}

const N: usize = 100;

fn heaviside(v: SMatrix<f64, N, 1>) -> SMatrix<f64, N, 1> {
    v.map(|i| i.signum())
}

fn thread_func(_thread_number: &usize, num_trials: &usize, steps: &usize) {
    let mut rng = rand::thread_rng();
    let m = SMatrix::<f64, N, N>::from_iterator((0..N * N).map(|_| rng.gen_range(-1.0..1.0)));

    for _trial_index in 0..*num_trials {
        // println!(
        //     "THREAD {:02} TRIAL: {:05}/{:05}",
        //     thread_number,
        //     trial_index + 1,
        //     num_trials
        // );
        let mut v = SVector::<f64, N>::from_iterator((0..N).map(|_| rng.gen_range(-1.0..1.0)));
        v = heaviside(v);

        for _step_index in 0..*steps {
            v = heaviside(m * v);
        }
    }
}

fn main() {
    let args = Args::parse();
    let trials_per_thread = args.trials / args.threads;
    let mut thread_handles = Vec::with_capacity(args.threads);

    for thread_index in 0..args.threads {
        thread_handles.push(thread::spawn(move || {
            thread_func(&thread_index, &trials_per_thread, &args.multiplications)
        }));
    }

    while !thread_handles.is_empty() {
        let curr_thread = thread_handles.remove(0);
        curr_thread.join().unwrap();
    }
}
