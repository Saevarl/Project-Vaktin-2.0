export interface GPU {
  name: string;
  link: string;
  model: string;
  price: string;
  store: string;
  manufacturer: string;
  date_checked: string;
  brand: string;
  series: string;
  vram: string;
  benchmark_score: number | null;
}

export interface Store {
  name: string;
  store_url: string;
  logo_url: string;
}

export interface GPUComparison {
  model: string;
  prices: { [storeName: string]: string | null };
  gpus: GPU[];
  benchmark_score: number | null;
}

