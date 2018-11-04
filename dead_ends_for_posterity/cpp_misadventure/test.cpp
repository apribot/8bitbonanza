// yes yes, bigboy bitwise warnings, we know.
#pragma GCC diagnostic ignored "-Wshift-count-overflow"

#include <cmath>
#include <fstream>
#include <iostream>
#include <string>
#include <sstream>
#include <vector>


using namespace std;

namespace little_endian_io
{
  template <typename Word>
  std::ostream& write_word( std::ostream& outs, Word value, unsigned size = sizeof( Word ) )
  {
    for (; size; --size, value >>= 8)
      outs.put( static_cast <char> (value & 0xFF) );
    return outs;
  }
}
using namespace little_endian_io;



vector< vector<string> > getSettings(string filename) {
    ifstream in(filename);
    string line, field;
    vector< vector<string> > array;  // the 2D array
    vector<string> v;                // array of values for one line only

    while ( getline(in,line) )    // get next line in file
    {
        v.clear();
        stringstream ss(line);
        while (getline(ss,field,',')) { // break line into comma delimitted fields
            v.push_back(field);  // add each field to the 1D array
        }
        array.push_back(v);  // add the 1D array to the 2D array
    }
    return array;
}



void makeWav(string filename, double noteOffset) {

  ofstream f( filename, ios::binary );

  // Write the file headers
  f << "RIFF----WAVEfmt ";     // (chunk size to be filled in later)
  write_word( f,     16, 4 );  // no extension data
  write_word( f,      1, 2 );  // PCM - integer samples
  write_word( f,      2, 2 );  // two channels (stereo file)
  write_word( f,  44100, 4 );  // samples per second (Hz)
  write_word( f, 176400, 4 );  // (Sample Rate * BitsPerSample * Channels) / 8
  write_word( f,      4, 2 );  // data block size (size of two integer samples, one for each channel, in bytes)
  write_word( f,     16, 2 );  // number of bits per sample (use a multiple of 8)

  // Write the data chunk header
  size_t data_chunk_pos = f.tellp();
  f << "data----";  // (chunk size to be filled in later)
  
  // Write the audio samples
  // (We'll generate a single C4 note with a sine wave, fading from left to right)
  constexpr double max_amplitude = 65536;  // "volume"

  double hz        = 44100;    // samples per second
  double frequency = 261.626;  // middle C
  double seconds   = 2.5;      // time

  double factor = pow(2.0 , (1.0 * noteOffset / 12.0));

  int N = (int) (hz * seconds) * (1/factor);  // total number of samples

  for (int i = 0; i < N; i++)
  {    

    int t = i * factor;

//    int a = (t*1000+t>>106|t*108)/(t+1);
//    int b = (t*(7+(1^t>>9%5)));

    int a = (t*(t>>9+t>>9)*100);
    int b = t;
    //int a = ((t/256)*(t/128))<<69;
    //int b = (t/128)*(t/16)/2;
    //int a = t;
    //int b = t;

    a = a % 255;
    b = b % 255;

    double point = (((a + b) / 2) * (max_amplitude / 255)) - (max_amplitude / 2);

    write_word( f, (int)point, 2 );
    write_word( f, (int)point, 2 );
  }
  
  // (We'll need the final file size to fix the chunk sizes above)
  size_t file_length = f.tellp();

  // Fix the data chunk header to contain the data size
  f.seekp( data_chunk_pos + 4 );
  write_word( f, file_length - data_chunk_pos + 8 );

  // Fix the file header to contain the proper RIFF chunk size, which is (file size - 8) bytes
  f.seekp( 0 + 4 );
  write_word( f, file_length - 8, 4 ); 


  //TODO: add in that garbage for the smpl loop points
}

int middleCOffsetToMIDINote(int offset) {
  return offset + (12 * 6); 
}

int main() {


  for (int note = (-4 * 12); note < (4 * 12) + 1; ++note) {
    makeWav( to_string(middleCOffsetToMIDINote(note)) + ".wav" , note);
    break;
  }
  
  /*
  vector< vector<string> > array = getSettings("settings.dat");
  for (size_t i=0; i<array.size(); ++i) {
    cout << "generating " << array[i][0];
    
    cout << "\n";
  }
  */



}
