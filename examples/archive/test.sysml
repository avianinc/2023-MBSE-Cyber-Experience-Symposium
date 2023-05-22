package Test {
    part partA;
    part partB{
        partC;
    }
    connect partA to partB;
}