function string=strip_char_2(string0)
    string='';
    for i=1:numel(string0)
        if (~strcmp(string0(i),'\n'))&&(abs(string0(i))~=8629) && (abs(string0(i))~=10) % 8629: the ascii of ?
            string=[string,string0(i)];
        end
    end
end 