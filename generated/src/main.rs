use std::arch::x86_64::*;

fn main(){
let mut total: i64 = 0;
for i in 0..10000000 {
total += i;
}
println!("{}", total);
}