describe('CI Pipeline Setup', () => {
  it('should pass a simple equality test', () => {
    expect(1 + 1).toBe(2);
  });

  it('should verify the testing environment', () => {
    expect(process.env.NODE_ENV).toBe('test');
  });
});
