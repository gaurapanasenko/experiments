#include <iostream>
#include <vector>
using namespace std;
class B;

class A {
public:
  vector<B*> b;
  A();
  void add(B* _b);


  ~A();
};

class B {
public:
  A *a;
  int x = 5;
  B() {
    printf("B");
  }

  ~B() {
    printf("~B");
    delete a;
  }
};

A::A() {
  printf("A");
};

void A::add(B* _b) {
  b.push_back(_b);
  _b->a = this;
}

A::~A() {
  printf("~A");
  for (int i = 0; i < b.size(); i++) {
    printf("\n%d : %d", b[i], b[i]->x);

    delete b[i];
  }
}

int main(int argc, char* argv[])
{
  A *a = new A();


  B *b;
  b = new B();
  a->add(b);

  delete a;
}
