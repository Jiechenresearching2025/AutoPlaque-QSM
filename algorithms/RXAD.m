function RXAD_map = RXAD(img0,K,uU,no_lines,no_rows)
[~,N]=size(img0);
RXADS = zeros(1,no_lines*no_rows);
for i=1:N
   r= img0(:,i);
   RXADS(1,i)=((r-uU)'*K*(r-uU));
end

RXAD_map = reshape(RXADS,[no_lines,no_rows]);
