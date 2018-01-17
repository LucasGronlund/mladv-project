#include <stdio.h>
#include <iostream>
#include <chrono>
#include <math.h>
#include <iomanip>


int n;
float l;

double *** mkMatrix(int height, int length, int depth)
{
	double *** tempMat = new double ** [height];
	for (int i = 0; i < height; ++i) {
		tempMat[i] = new double*[length];
    for (int j = 0; j < length; ++j) {
  		tempMat[i][j] = new double[depth];
   	}
 	}
 	return tempMat;
}

double ** mkMatrix(int height, int length)
{
	double ** tempMat = new double * [height];
	for (int i = 0; i < height; ++i) tempMat[i] = new double[length];
 	return tempMat;
}

void cleanMatrix(double *** theMat, int height, int length, int depth)
{
  for (int i = 0; i < height; i++)
    for (int j = 0; j < length; j++)
      for (int k = 0; k < depth; k++)
        theMat[0][0][0] = 0;
}

void printmatrix(double** matrix, int height, int length)
{
	std::cout << height << " " << length;
	for(int row = 0; row < height; row = row +1)
	{
		for(int col = 0; col < length; col = col +1)
		{
			std::cout << " " << std::setprecision(32) << matrix[row][col];
		}
	}
	std::cout << "\n";
}

void k_prime(char* s, char* t, int n, double l, int s_len, int t_len, double *** kp, double *** kpp)
{
    // Make first row of ones.
    int i = 0, j = 0, k = 0;

    for (j = 0; j < s_len + 1; j++)
    {
      for (k = 0; k < t_len + 1; k++)
      {
        kp[0][j][k] = 1;
      }
    }



    for (i = 1; i < n; i++)
    {
      for (j = i; j < s_len; j++)
      {
        for (k = i; k < t_len + 1; k++)
        {
          if (s[j-1] != t[k-1])
          {
            kpp[i][j][k] = l*kpp[i][j][k-1];

          } else
          {
            kpp[i][j][k] = l*(kpp[i][j][k-1] + l*kp[i-1][j-1][k-1]);

          }
          kp[i][j][k-1]=l*kp[i][j-1][k-1]+kpp[i][j][k-1];

        }
      }
    }
    cleanMatrix(kpp, n, s_len, t_len);
}

double k (char* s, char* t, int n, double l, int s_len, int t_len, double *** kp)
{
  double ksum = 0;


  for (int i = 0; i < s_len; i++)
  {
    for (int j = 0; j < t_len; j++)
    {
      if (s[i] == t[j])
      {
        ksum += kp[n-1][i][j];
      }
    }
  }
  return l*l*ksum;
}

double ** kernelValuesListChptr6(char** x, char** s, int n, double l, int x_number_of_str, int s_number_of_str, int* x_lens, double *** kp, double *** kpp)
{
	double ** out = mkMatrix(x_number_of_str,s_number_of_str);
	for (int i = 0; i < x_number_of_str; i++)
	{
		for (int j = 0; j < s_number_of_str; j++)
		{
			k_prime(x[i],s[j],n,l,x_lens[i],n,kp,kpp);
    	out[i][j]= k(x[i],s[j],n,l,x_lens[i],n,kp);
      cleanMatrix(kp, n, x_lens[i], n);
		}
	}
	return out;
}

double ** approximative_kernel(char** x, char** z, char** s, int n, double l, int x_number_of_str, int z_number_of_str, int s_number_of_str, int* x_lens, int* z_lens, double *** kp, double *** kpp, int equal_hash)
{
	double ** K = mkMatrix(x_number_of_str,z_number_of_str);
  double * kss = new double[s_number_of_str];
  double * kxx = new double[x_number_of_str];
	double ** kxs = kernelValuesListChptr6(x, s, n, l, x_number_of_str, s_number_of_str, x_lens, kp, kpp);

  for (int i = 0; i < s_number_of_str; i++)
  {
    k_prime(s[i],s[i],n,l,n,n,kp,kpp); // calculate _k(i,i,n,l,_k_prime(i,i,n,l))
    kss[i] = k(s[i],s[i],n,l,n,n,kp);
    cleanMatrix(kp, n, n, n);
  }
  for (int i = 0; i < x_number_of_str; i++)
  {
    k_prime(x[i],x[i],n,l,x_lens[i],x_lens[i],kp,kpp); // calculate _k(i,i,n,l,_k_prime(i,i,n,l))
    kxx[i] = k(x[i],x[i],n,l,x_lens[i],x_lens[i],kp);
    cleanMatrix(kp, n, x_lens[i], x_lens[i]);
  }


	if (equal_hash == 1)
	{
		for (int i = 0; i < x_number_of_str; i++) K[i][i] = 1; // np.ientity(N)
		for (int i = 0; i < x_number_of_str; i++)
    {
      for (int j = i + 1; j < z_number_of_str; j++)
      {
				for (int k = 0; k < s_number_of_str; k++)
	      {
	        K[i][j] += (kxs[i][k] * kxs[j][k])/(kss[k]*sqrt(kxx[j]*kxx[i]));
	        K[j][i] = K[i][j];
				}
      }
    }
	} else
	{
		double * kzz = new double[z_number_of_str];
		for (int i = 0; i < z_number_of_str; i++)
	  {
	    k_prime(z[i],z[i],n,l,z_lens[i],z_lens[i],kp,kpp); // calculate _k(i,i,n,l,_k_prime(i,i,n,l))
	    kzz[i] = k(z[i],z[i],n,l,z_lens[i],z_lens[i],kp);
	    cleanMatrix(kp, n, z_lens[i], z_lens[i]);
	  }
	  double ** kzs = kernelValuesListChptr6(z, s, n, l, z_number_of_str, s_number_of_str, z_lens, kp, kpp);
		for (int i = 0; i < x_number_of_str; i++)
    {
      for (int j = 0; j < z_number_of_str; j++)
      {
				for (int k = 0; k < s_number_of_str; k++)
	      {
	        K[i][j] += (kxs[i][k] * kzs[j][k])/(kss[k]*sqrt(kzz[j]*kxx[i]));
				}
      }
    }
	}
	return K;
}

// double ** recursive_kernel(char** s, char** t, int n, double l, int s_number_of_str, int t_number_of_str, int* s_lens, int* t_lens, double *** kp, double *** kpp)
// {
//   double ** K = mkMatrix(s_number_of_str,t_number_of_str);
//   double * kss = new double[s_number_of_str];
//   double * ktt = new double[t_number_of_str];
//
//   if (s_number_of_str != t_number_of_str)
//   {
//     double kst = 0;
//
//     for (int i = 0; i < s_number_of_str; i++)
//     {
//       k_prime(s[i],s[i],n,l,s_lens[i],s_lens[i],kp,kpp); // calculate _k(i,i,n,l,_k_prime(i,i,n,l))
//       kss[i] = k(s[i],s[i],n,l,s_lens[i],s_lens[i],kp);
//       cleanMatrix(kp, n, s_lens[i], s_lens[i]);
//     }
//     for (int i = 0; i < t_number_of_str; i++)
//     {
//       k_prime(t[i],t[i],n,l,t_lens[i],t_lens[i],kp,kpp); // calculate _k(i,i,n,l,_k_prime(i,i,n,l))
//       ktt[i] = k(t[i],t[i],n,l,t_lens[i],t_lens[i],kp);
//       cleanMatrix(kp, n, t_lens[i], t_lens[i]);
//     }
//     for (int i = 0; i < s_number_of_str; i++)
//     {
//       for (int j = 0; j < t_number_of_str; j++)
//       {
//         // s_temp[0] = s[i]; t_temp[0] = t[j];
//         k_prime(s[i],t[j],n,l,s_lens[i],t_lens[j],kp,kpp);
//         kst = k(s[i],t[j],n,l,s_lens[i],t_lens[j],kp);
//         cleanMatrix(kp, n, s_lens[i],t_lens[j]);
//         K[i][j] = kst/sqrt(kss[i]*ktt[j]);
//       }
//     }
//
//
//   } else
//   {
//     double kst = 0;
//     for (int i = 0; i < s_number_of_str; i++) K[i][i] = 1; // np.ientity(N)
//
//     for (int i = 0; i < s_number_of_str; i++)
//     {
//       k_prime(s[i],s[i],n,l,s_lens[i],s_lens[i],kp,kpp); // calculate _k(i,i,n,l,_k_prime(i,i,n,l))
//       kss[i] = k(s[i],s[i],n,l,s_lens[i],s_lens[i],kp);
//       cleanMatrix(kp, n, s_lens[i], s_lens[i]);
//     }
//
//     for (int i = 0; i < s_number_of_str; i++)
//     {
//       for (int j = i + 1; j < s_number_of_str; j++)
//       {
//         k_prime(s[i],t[j],n,l,s_lens[i],t_lens[j],kp,kpp);
//         kst = k(s[i],t[j],n,l,s_lens[i],t_lens[j],kp);
//         cleanMatrix(kp, n, s_lens[i],t_lens[j]);
//
//         K[i][j] = kst/sqrt(kss[i]*kss[j]);
//         K[j][i] = K[i][j];
//       }
//     }
//
//   }
//   return K;
// }

// double ** approximate_kernel()

int main() {
  std::chrono::steady_clock::time_point begin = std::chrono::steady_clock::now();

  int equal_hash = 0;
  (void) scanf("%d",&equal_hash);


  int x_number_of_strings = 0;
  int z_number_of_strings = 0;
	int s_number_of_strings = 0;


  (void) scanf("%d %d %d",&x_number_of_strings, &z_number_of_strings, &s_number_of_strings);

  char ** x_features = new char * [x_number_of_strings];
  char ** z_features = new char * [z_number_of_strings];
	char ** s_features = new char * [s_number_of_strings];

	int * x_string_lengths = new int[x_number_of_strings];
	int * z_string_lengths = new int[z_number_of_strings];
  int * s_string_lengths = new int[s_number_of_strings];

  int all_string_lengths_max = 0;
  // int t_string_lengths_max = 0;

	for (int i = 0; i < x_number_of_strings; i++)
	{
		(void) scanf("%d",&x_string_lengths[i]);
		x_features[i] = new char[x_string_lengths[i]];
		if (x_string_lengths[i] > all_string_lengths_max){
			all_string_lengths_max = x_string_lengths[i];
		}
	}
	for (int i = 0; i < z_number_of_strings; i++)
  {
    (void) scanf("%d",&z_string_lengths[i]);
    z_features[i] = new char[z_string_lengths[i]];
    if (z_string_lengths[i] > all_string_lengths_max){
      all_string_lengths_max = z_string_lengths[i];
    }
  }
  for (int i = 0; i < s_number_of_strings; i++)
  {
    (void) scanf("%d",&s_string_lengths[i]);
    s_features[i] = new char[s_string_lengths[i]];
    if (s_string_lengths[i] > all_string_lengths_max){
      all_string_lengths_max = s_string_lengths[i];
    }
  }


  n = 0; l = 0;

  (void) scanf("%d %f", &n, &l);
  double *** kp = NULL;
  double *** kpp = NULL;

  for (int i = 0; i < x_number_of_strings; i++)
    for (int j = 0; j < x_string_lengths[i]; j++)
      (void) scanf("%c", &x_features[i][j]);

	for (int i = 0; i < z_number_of_strings; i++)
    for (int j = 0; j < z_string_lengths[i]; j++)
      (void) scanf("%c", &z_features[i][j]);

	for (int i = 0; i < s_number_of_strings; i++)
    for (int j = 0; j < s_string_lengths[i]; j++)
      (void) scanf("%c", &s_features[i][j]);

	// std::cout << "Hello" << std::endl;

  kp = mkMatrix(n, all_string_lengths_max + 1, all_string_lengths_max + 1);
  kpp = mkMatrix(n, all_string_lengths_max + 1, all_string_lengths_max + 1);

	double ** K = approximative_kernel(x_features, z_features, s_features, n, l, x_number_of_strings, z_number_of_strings, s_number_of_strings, x_string_lengths, z_string_lengths, kp, kpp, equal_hash);
	printmatrix(K,x_number_of_strings,z_number_of_strings);
  // double ** K = recursive_kernel(s_features,  t_features, n, l, s_number_of_strings, t_number_of_strings, s_string_lengths, t_string_lengths, kp, kpp);


  std::chrono::steady_clock::time_point end= std::chrono::steady_clock::now();
  std::cout << "Total time: " << std::chrono::duration_cast<std::chrono::microseconds>(end - begin).count()/1000 << " ms" << std::endl;
  std::cout << "Time difference = " << std::chrono::duration_cast<std::chrono::nanoseconds> (end - begin).count() << " ns" <<std::endl;
}
