#include <stdio.h>
#include <iostream>
#include <chrono>
#include <math.h>



// = 854;
int n;// = 10;
float l;// = 0.5;

double ** K = NULL;
//
// char s_test[] = "det var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och hadet var en gang en apa och ha";
// char t_test[] = "jag var en apajag var en apajag var en apajag var en apajag var en apajag var en apajag var en apajag var en apajag var en apajag var en apajag var en apajag var en apajag var en apajag var en apajag var en apajag var en apajag var en apajag var en apajag var en apajag var en apajag var en apajag var en apajag var en apajag var en apajag var en apajag var en apajag var en apajag var en apajag var en apajag var en apajag var en apajag var en apajag var en apajag var en apajag var en apajag var en apajag var en apajag var en apajag var en apajag var en apajag var en apajag var en apajag var en apajag var en apajag var en apajag var en apajag var en apajag var en apajag var en apajag var en apajag var en apajag var en apajag var en apajag var en apajag var en apajag var en apajag var en apajag var en apajag var en apajag var en apajag var en apa";

// char * s;
// char * t;

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
	for (int i = 0; i < height; ++i) {
		tempMat[i] = new double[length];
 	}
 	return tempMat;
}

void cleanMatrix(double *** theMat, int height, int length, int depth)
{
  for (int i = 0; i < height; i++)
  {
    for (int j = 0; j < length; j++)
    {
      for (int k = 0; k < depth; k++)
      {
        theMat[0][0][0] = 0;
      }
    }
  }
}

void printmatrix(double** matrix, int height, int length)
{
	std::cout << height << " " << length;
	for(int row = 0; row < height; row = row +1)
	{
		for(int col = 0; col < length; col = col +1)
		{
			std::cout << " " << matrix[row][col];
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

double ** recursive_kernel(char** s, char** t, int n, double l, int s_number_of_str, int t_number_of_str, int* s_lens, int* t_lens, double *** kp, double *** kpp)
{
  K = mkMatrix(s_len,t_len);
  double * kss = new double[s_number_of_str];
  double * ktt = new double[t_number_of_str];

  // char * s_temp = new char[1];
  // char * t_temp = new char[1];


  if (s_number_of_str != t_number_of_str)
  {
    double kst = 0;
    for (int i = 0; i < s_number_of_str; i++)
    {
      k_prime(s_temp,s_temp,n,l,1,1,kp,kpp); // calculate _k(i,i,n,l,_k_prime(i,i,n,l))
      kss[i] = k(s_temp,s_temp,n,l,1,1,kp);
      cleanMatrix(kp, n, 1, 1);
    }
    for (int i = 0; i < t_number_of_str; i++)
    {
      t_temp[0] = t[i];
      k_prime(t_temp,t_temp,n,l,1,1,kp,kpp); // calculate _k(i,i,n,l,_k_prime(i,i,n,l))
      ktt[i] = k(t_temp,t_temp,n,l,1,1,kp);
      cleanMatrix(kp, n, 1, 1);
    }
    for (int i = 0; i < s_len; i++)
    {
      for (int j = 0; j < t_len; j++)
      {
        s_temp[0] = s[i]; t_temp[0] = t[j];
        k_prime(s_temp,t_temp,n,l,1,1,kp,kpp);
        kst = k(s_temp,t_temp,n,l,1,1,kp);
        cleanMatrix(kp, n, 1, 1);
        K[i][j] = kst/sqrt(kss[i]*ktt[j]);
      }
    }


  } else
  {
    for (int i = 0; i < s_len; i++) K[i][i] = 1; // np.ientity(N)
  }
  return K;
}

int main() {
  std::chrono::steady_clock::time_point begin = std::chrono::steady_clock::now();

  int s_number_of_strings = 0;
  int t_number_of_strings = 0;


  (void) scanf("%d %d",&s_number_of_strings, &t_number_of_strings);
  std::cout << s_number_of_strings << std::endl;
  std::cout << t_number_of_strings << std::endl;

  char ** s_features = new char * [s_number_of_strings];
  char ** t_features = new char * [t_number_of_strings];

  int * s_string_lengths = new int[s_number_of_strings];
  int * t_string_lengths = new int[t_number_of_strings];

  for (int i = 0; i < s_number_of_strings; i++)
  {
    (void) scanf("%d",&s_string_lengths[i]);
    s_features[i] = new char[s_string_lengths[i]];
    // std::cout << s_string_lengths[i] << std::endl;
  }
  for (int i = 0; i < t_number_of_strings; i++)
  {
    (void) scanf("%d",&t_string_lengths[i]);
    t_features[i] = new char[t_string_lengths[i]];
    // std::cout << t_string_lengths[i] << std::endl;
  }


  n = 0; l = 0;

  (void) scanf("%d %f", &n, &l);
  double *** kp = NULL;
  double *** kpp = NULL;
  std::cout << n << std::endl;
  std::cout << l << std::endl;

  for (int i = 0; i < s_number_of_strings; i++)
    for (int j = 0; j < s_string_lengths[i]; j++)
      (void) scanf("%c", &s_features[i][j]);


  for (int i = 0; i < t_number_of_strings; i++)
    for (int j = 0; j < t_string_lengths[i]; j++)
      (void) scanf("%c", &t_features[i][j]);

  // for (int i = 0; i < number_of_strings; i++)
  // {
  //   kp = mkMatrix(n, the_s_len + 1, the_t_len + 1);
  //   kpp = mkMatrix(n, the_s_len + 1, the_s_len + 1);
  // }
  // int the_s_len;// = 1769;
  // int the_t_len;
  // double *** kp = NULL;
  // double *** kpp = NULL;
  // std::chrono::steady_clock::time_point begin = std::chrono::steady_clock::now();
  // n = 0; l = 0; the_s_len = 0; the_t_len = 0;
  // (void) scanf("%d %d %d %f", &the_s_len, &the_t_len, &n, &l);
  /////////////////
  // s = new char[the_s_len];
  // t = new char[the_t_len];
  // for (int i = 0; i < the_s_len; i++) (void) scanf("%c", &s[i]);
  // for (int i = 0; i < the_t_len; i++) (void) scanf("%c", &t[i]);

  // std::cout << the_s_len << std::endl;
  // std::cout << the_t_len << std::endl;



  // kp = mkMatrix(n, the_s_len + 1, the_t_len + 1);
  // kpp = mkMatrix(n, the_s_len + 1, the_s_len + 1);
  //
  //
  // // k_prime(s_test, t_test, n, l, the_s_len, the_t_len, kp, kpp);
  // // std::cout << k (s_test, t_test, n, l, the_s_len, the_t_len, kp) << std::endl;
  //
  // recursive_kernel(s_test,  t_test, n, l, the_s_len, the_t_len, kp, kpp);






  std::chrono::steady_clock::time_point end= std::chrono::steady_clock::now();
  std::cout << "Total time: " << std::chrono::duration_cast<std::chrono::microseconds>(end - begin).count()/1000 << " ms" << std::endl;
  std::cout << "Time difference = " << std::chrono::duration_cast<std::chrono::nanoseconds> (end - begin).count() << " ns" <<std::endl;
}
