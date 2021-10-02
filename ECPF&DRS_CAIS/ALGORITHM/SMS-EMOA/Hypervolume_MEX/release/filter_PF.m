function filtered_pf = filter_PF(PF,w_point, ref_point, radius)
    min_d = Inf;
    filtered_pf = [];
    d1 = norm(w_point - ref_point);
    for i = 1 : size(PF,1)
        d2 = norm(PF(i,:) - ref_point);
        d3 = norm(PF(i,:) - w_point);
        p = 0.5 * (d1 + d2 + d3);
        d = 2 * (p*(p-d1)*(p-d2)*(p-d3))^0.5 / d1;
        if d < min_d
            min_d = d;
            pf_center = PF(i,:);
        end
    end    
    k = 1;
    for i = 1 : size(PF,1)
        if norm(PF(i,:)-pf_center) <= radius/2.0
            filtered_pf(k,:) = PF(i,:);
            k = k + 1;
        end
    end
end